from pathlib import Path

import requests
from bs4 import BeautifulSoup


SOURCE_URLS = {
    "adf_migration_planning": (
        "https://learn.microsoft.com/en-us/fabric/data-factory/"
        "migrate-planning-azure-data-factory"
    ),
    "adf_migration_assessment": (
        "https://learn.microsoft.com/en-us/azure/data-factory/"
        "how-to-assess-your-azure-data-factory-to-fabric-data-factory-migration"
    ),
    "synapse_spark_migration": (
        "https://learn.microsoft.com/en-us/fabric/data-engineering/"
        "migrate-synapse-overview"
    ),
    "adf_migration_best_practices": (
        "https://learn.microsoft.com/en-us/fabric/data-factory/"
        "migration-best-practices"
    ),
}


OUTPUT_DIR = Path("knowledge/processed")


def fetch_page(url: str) -> str:
    """
    Download the HTML content of a Microsoft Learn page.
    """
    response = requests.get(
        url,
        timeout=30,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        },
    )

    response.encoding = response.apparent_encoding
    response.raise_for_status()

    return response.text


def extract_article_text(html: str) -> tuple[str, str]:
    """
    Extract the main article title and readable article text.
    """
    soup = BeautifulSoup(html, "html.parser")

    title = (
        soup.title.get_text(" ", strip=True)
        if soup.title
        else "Untitled"
    )

    article = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", {"class": "content"})
    )

    if article is None:
        article = soup

    for tag in article(
        [
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "form",
            "button",
            "aside",
        ]
    ):
        tag.decompose()

    text = article.get_text(
        separator="\n",
        strip=True,
    )

    cleaned_lines = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)

    return title, cleaned_text


def save_document(
    name: str,
    title: str,
    url: str,
    text: str,
) -> None:
    """
    Save cleaned article text with source metadata.
    """
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = OUTPUT_DIR / f"{name}.txt"

    content = f"""TITLE: {title}
SOURCE_URL: {url}
SOURCE_TYPE: Microsoft Learn

============================================================

{text}
"""

    output_file.write_text(
        content,
        encoding="utf-8",
    )

    print(f"Saved: {output_file}")


def ingest_all() -> None:
    """
    Fetch, clean, and save all configured knowledge sources.
    """
    for name, url in SOURCE_URLS.items():

        print("=" * 70)
        print(f"Processing: {name}")
        print(f"URL: {url}")

        try:
            html = fetch_page(url)

            title, text = extract_article_text(html)

            save_document(
                name=name,
                title=title,
                url=url,
                text=text,
            )

            print(
                f"Characters extracted: {len(text)}"
            )

        except requests.RequestException as exc:
            print(
                f"HTTP error for {name}: {exc}"
            )

        except Exception as exc:
            print(
                f"Unexpected error for {name}: {exc}"
            )


if __name__ == "__main__":
    ingest_all()