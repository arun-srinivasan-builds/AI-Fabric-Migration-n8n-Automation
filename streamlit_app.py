import ast
import csv
import json
from typing import Any

import pandas as pd
import requests
import streamlit as st


# =========================================================
# Application Configuration
# =========================================================

WEBHOOK_URL = (
    "https://n8n.srv1965124.hstgr.cloud/"
    "webhook/fabric-migration-assessment"
)

REQUIRED_COLUMNS = [
    "project_id",
    "application_name",
    "source_platform",
    "workload_type",
    "data_size_gb",
    "daily_jobs",
    "dependencies",
    "business_criticality",
    "current_issues",
    "target_platform",
]


st.set_page_config(
    page_title="Fabric Migration Assessment Platform",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

html, body, [class*="css"] {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

.stApp {
    background: #f8fafc;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ---------------------------------------------------------
   HERO
--------------------------------------------------------- */

.hero {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(
            120deg,
            #0f172a 0%,
            #172554 48%,
            #2563eb 100%
        );
    border-radius: 22px;
    padding: 2.5rem 2.7rem;
    margin-bottom: 1.7rem;
    box-shadow:
        0 20px 50px rgba(15, 23, 42, 0.15);
}

.hero::after {
    content: "";
    position: absolute;
    width: 360px;
    height: 360px;
    border-radius: 50%;
    right: -130px;
    top: -190px;
    background:
        rgba(147, 197, 253, 0.16);
}

.hero-eyebrow {
    color: #93c5fd;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.75rem;
    font-weight: 750;
    margin-bottom: 0.8rem;
}

.hero-title {
    color: white;
    font-size: 2.45rem;
    line-height: 1.12;
    font-weight: 760;
    max-width: 1000px;
    margin-bottom: 0.8rem;
}

.hero-subtitle {
    color: #dbeafe;
    font-size: 1.02rem;
    line-height: 1.65;
    max-width: 1050px;
}

.hero-status {
    display: inline-block;
    margin-top: 1.3rem;
    padding: 0.42rem 0.8rem;
    border-radius: 999px;
    background:
        rgba(255, 255, 255, 0.10);
    border:
        1px solid rgba(255, 255, 255, 0.16);
    color: #e0f2fe;
    font-size: 0.8rem;
    font-weight: 650;
}


/* ---------------------------------------------------------
   SECTION HEADERS
--------------------------------------------------------- */

.section-kicker {
    color: #2563eb;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-size: 0.7rem;
    font-weight: 800;
    margin-bottom: 0.25rem;
}

.section-title {
    color: #0f172a;
    font-size: 1.42rem;
    font-weight: 750;
    margin-bottom: 0.3rem;
}

.section-description {
    color: #64748b;
    font-size: 0.9rem;
    line-height: 1.55;
    margin-bottom: 1rem;
}


/* ---------------------------------------------------------
   CARDS
--------------------------------------------------------- */

.card {
    height: 100%;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.2rem 1.25rem;
    box-shadow:
        0 4px 14px rgba(15, 23, 42, 0.045);
}

.card-number {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: #eff6ff;
    color: #2563eb;
    font-size: 0.78rem;
    font-weight: 800;
    margin-bottom: 0.8rem;
}

.card-title {
    color: #0f172a;
    font-size: 0.96rem;
    font-weight: 720;
    margin-bottom: 0.35rem;
}

.card-text {
    color: #64748b;
    font-size: 0.82rem;
    line-height: 1.5;
}


/* ---------------------------------------------------------
   ARCHITECTURE
--------------------------------------------------------- */

.architecture-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.3rem;
    box-shadow:
        0 4px 14px rgba(15, 23, 42, 0.04);
}

.architecture-text {
    color: #64748b;
    font-size: 0.84rem;
    line-height: 1.55;
}

.tech-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1rem;
}

.tech-pill {
    display: inline-block;
    background: #eff6ff;
    color: #1e40af;
    border: 1px solid #bfdbfe;
    border-radius: 999px;
    padding: 0.36rem 0.72rem;
    font-size: 0.75rem;
    font-weight: 650;
}


/* ---------------------------------------------------------
   UPLOAD PANEL
--------------------------------------------------------- */

.upload-panel {
    background: white;
    border: 1px solid #dbe4f0;
    border-radius: 16px;
    padding: 1.2rem 1.3rem;
    margin-bottom: 1rem;
}

.upload-heading {
    color: #0f172a;
    font-size: 0.95rem;
    font-weight: 720;
    margin-bottom: 0.35rem;
}

.upload-copy {
    color: #64748b;
    font-size: 0.84rem;
    line-height: 1.55;
}


/* ---------------------------------------------------------
   METRICS
--------------------------------------------------------- */

.metric-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.15rem;
    min-height: 124px;
    box-shadow:
        0 4px 14px rgba(15, 23, 42, 0.045);
}

.metric-label {
    color: #64748b;
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    font-weight: 750;
}

.metric-value {
    color: #0f172a;
    font-size: 2rem;
    font-weight: 760;
    margin-top: 0.5rem;
}

.metric-note {
    color: #94a3b8;
    font-size: 0.75rem;
    margin-top: 0.3rem;
}

.metric-high {
    border-top: 4px solid #dc2626;
}

.metric-medium {
    border-top: 4px solid #f59e0b;
}

.metric-low {
    border-top: 4px solid #16a34a;
}

.metric-review {
    border-top: 4px solid #7c3aed;
}


/* ---------------------------------------------------------
   RISK BADGES
--------------------------------------------------------- */

.badge-high,
.badge-medium,
.badge-low,
.badge-unknown {
    display: inline-block;
    border-radius: 999px;
    padding: 0.28rem 0.65rem;
    font-size: 0.76rem;
    font-weight: 750;
}

.badge-high {
    background: #fef2f2;
    color: #b91c1c;
    border: 1px solid #fecaca;
}

.badge-medium {
    background: #fffbeb;
    color: #b45309;
    border: 1px solid #fde68a;
}

.badge-low {
    background: #f0fdf4;
    color: #15803d;
    border: 1px solid #bbf7d0;
}

.badge-unknown {
    background: #f8fafc;
    color: #475569;
    border: 1px solid #cbd5e1;
}


/* ---------------------------------------------------------
   HIGH-RISK ALERT
--------------------------------------------------------- */

.high-risk-alert {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-left: 5px solid #dc2626;
    border-radius: 14px;
    padding: 1rem 1.15rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.high-risk-alert-title {
    color: #991b1b;
    font-size: 0.95rem;
    font-weight: 750;
}

.high-risk-alert-text {
    color: #7f1d1d;
    font-size: 0.82rem;
    line-height: 1.5;
    margin-top: 0.25rem;
}


/* ---------------------------------------------------------
   DETAILS
--------------------------------------------------------- */

.detail-grid {
    display: grid;
    grid-template-columns:
        repeat(3, minmax(0, 1fr));
    gap: 0.8rem;
    margin-bottom: 1rem;
}

.detail-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 0.85rem;
}

.detail-label {
    color: #64748b;
    font-size: 0.68rem;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.detail-value {
    color: #0f172a;
    font-size: 0.9rem;
    font-weight: 650;
    margin-top: 0.25rem;
}


/* ---------------------------------------------------------
   NOTES
--------------------------------------------------------- */

.governance-note {
    background: #f8fafc;
    border-left: 4px solid #2563eb;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    color: #475569;
    font-size: 0.84rem;
    line-height: 1.55;
}

.download-note {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    color: #1e3a8a;
    font-size: 0.82rem;
    line-height: 1.5;
}


/* ---------------------------------------------------------
   BUTTONS
--------------------------------------------------------- */

div.stButton > button {
    width: 100%;
    min-height: 46px;
    border-radius: 10px;
    font-weight: 700;
}

div.stDownloadButton > button {
    width: 100%;
    min-height: 46px;
    border-radius: 10px;
    font-weight: 700;
}


/* ---------------------------------------------------------
   FOOTER
--------------------------------------------------------- */

.enterprise-footer {
    text-align: center;
    color: #64748b;
    border-top: 1px solid #e2e8f0;
    margin-top: 2.7rem;
    padding-top: 1.5rem;
    font-size: 0.78rem;
    line-height: 1.7;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# Helper Functions
# =========================================================

def html(content: str) -> None:
    """
    Render custom HTML without Markdown indentation issues.
    """

    st.markdown(
        content.replace("\n", ""),
        unsafe_allow_html=True,
    )


def decode_csv_bytes(
    file_bytes: bytes,
) -> str:
    """
    Decode CSV using common encodings.
    """

    for encoding in [
        "utf-8-sig",
        "utf-8",
        "cp1252",
        "latin-1",
    ]:
        try:
            return file_bytes.decode(
                encoding
            )
        except UnicodeDecodeError:
            continue

    return file_bytes.decode(
        "utf-8",
        errors="replace",
    )


def parse_csv_bytes(
    file_bytes: bytes,
) -> pd.DataFrame:
    """
    Parse CSV robustly.

    This also handles the single-column CSV issue
    previously seen in Streamlit and n8n.
    """

    text = decode_csv_bytes(
        file_bytes
    )

    text = (
        text
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )

    lines = [
        line
        for line in text.split("\n")
        if line.strip()
    ]

    if not lines:
        return pd.DataFrame()

    rows = list(
        csv.reader(
            lines,
            delimiter=",",
            quotechar='"',
        )
    )

    if not rows:
        return pd.DataFrame()

    header = [
        str(column).strip()
        for column in rows[0]
    ]

    data_rows = rows[1:]


    if (
        len(header) == 1
        and "," in header[0]
    ):

        header = next(
            csv.reader(
                [header[0]],
                delimiter=",",
                quotechar='"',
            )
        )

        reparsed_rows = []

        for row in data_rows:

            raw_line = (
                row[0]
                if len(row) == 1
                else ",".join(row)
            )

            parsed_row = next(
                csv.reader(
                    [raw_line],
                    delimiter=",",
                    quotechar='"',
                )
            )

            reparsed_rows.append(
                parsed_row
            )

        data_rows = (
            reparsed_rows
        )


    normalized_rows = []

    for row in data_rows:

        if len(row) < len(header):

            row = row + (
                [""] *
                (
                    len(header)
                    - len(row)
                )
            )

        elif len(row) > len(header):

            row = (
                row[: len(header) - 1]
                + [
                    ",".join(
                        row[
                            len(header) - 1:
                        ]
                    )
                ]
            )

        normalized_rows.append(
            row
        )


    dataframe = pd.DataFrame(
        normalized_rows,
        columns=[
            str(column).strip()
            for column in header
        ],
    )

    return dataframe


def validate_inventory(
    dataframe: pd.DataFrame,
) -> tuple[bool, list[str]]:
    """
    Validate required inventory structure.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    return (
        len(missing_columns) == 0,
        missing_columns,
    )


def combine_inventory_files(
    uploaded_files,
) -> tuple[
    pd.DataFrame,
    list[str],
    list[str],
]:
    """
    Parse and combine multiple inventory CSV files.

    Returns:
        combined_dataframe
        valid_file_names
        validation_errors
    """

    frames = []
    valid_file_names = []
    validation_errors = []


    for uploaded_file in uploaded_files:

        try:

            file_bytes = (
                uploaded_file.getvalue()
            )

            dataframe = (
                parse_csv_bytes(
                    file_bytes
                )
            )

            valid, missing_columns = (
                validate_inventory(
                    dataframe
                )
            )


            if not valid:

                validation_errors.append(
                    f"{uploaded_file.name}: "
                    f"missing {', '.join(missing_columns)}"
                )

                continue


            dataframe = dataframe[
                REQUIRED_COLUMNS
            ].copy()


            frames.append(
                dataframe
            )

            valid_file_names.append(
                uploaded_file.name
            )


        except Exception as exc:

            validation_errors.append(
                f"{uploaded_file.name}: {exc}"
            )


    if not frames:

        return (
            pd.DataFrame(),
            valid_file_names,
            validation_errors,
        )


    combined_dataframe = pd.concat(
        frames,
        ignore_index=True,
    )


    return (
        combined_dataframe,
        valid_file_names,
        validation_errors,
    )


def dataframe_to_csv_bytes(
    dataframe: pd.DataFrame,
) -> bytes:
    """
    Convert combined inventory dataframe to CSV bytes.
    """

    csv_text = dataframe.to_csv(
        index=False,
    )

    return csv_text.encode(
        "utf-8"
    )


def clean_cell(
    value: Any,
) -> str:

    if value is None:
        return "Not available"

    try:
        if pd.isna(value):
            return "Not available"
    except TypeError:
        pass

    value = str(
        value
    ).strip()

    if not value:
        return "Not available"

    return value


def clean_collection(
    value: Any,
) -> list[str]:

    if value is None:
        return []

    try:
        if pd.isna(value):
            return []
    except TypeError:
        pass


    if isinstance(
        value,
        list,
    ):

        return [
            str(item)
            for item in value
        ]


    text = str(
        value
    ).strip()


    if not text:
        return []


    try:

        parsed = json.loads(
            text
        )

        if isinstance(
            parsed,
            list,
        ):

            return [
                str(item)
                for item in parsed
            ]

    except Exception:
        pass


    try:

        parsed = ast.literal_eval(
            text
        )

        if isinstance(
            parsed,
            list,
        ):

            return [
                str(item)
                for item in parsed
            ]

    except Exception:
        pass


    if ";" in text:

        return [
            item.strip()
            for item in text.split(";")
            if item.strip()
        ]


    return [text]


def risk_badge(
    risk_level: str,
) -> str:

    risk = (
        str(risk_level)
        .strip()
        .lower()
    )


    if risk == "high":

        return (
            '<span class="badge-high">'
            'HIGH RISK'
            '</span>'
        )


    if risk == "medium":

        return (
            '<span class="badge-medium">'
            'MEDIUM RISK'
            '</span>'
        )


    if risk == "low":

        return (
            '<span class="badge-low">'
            'LOW RISK'
            '</span>'
        )


    return (
        '<span class="badge-unknown">'
        'UNCLASSIFIED'
        '</span>'
    )


def risk_sort_value(
    risk_level: str,
) -> int:

    return {
        "high": 1,
        "medium": 2,
        "low": 3,
    }.get(
        str(risk_level)
        .strip()
        .lower(),
        4,
    )


def highlight_risk_rows(
    row: pd.Series,
) -> list[str]:
    """
    Highlight portfolio result rows by risk.
    """

    risk = str(
        row.get(
            "risk_level",
            "",
        )
    ).strip().lower()


    if risk == "high":

        style = (
            "background-color: #fee2e2; "
            "color: #991b1b; "
            "font-weight: 700;"
        )


    elif risk == "medium":

        style = (
            "background-color: #fef3c7; "
            "color: #92400e;"
        )


    elif risk == "low":

        style = (
            "background-color: #dcfce7; "
            "color: #166534;"
        )


    else:

        style = ""


    return [
        style
        for _ in row
    ]


# =========================================================
# Session State
# =========================================================

if "assessment_df" not in st.session_state:
    st.session_state.assessment_df = None

if "assessment_csv" not in st.session_state:
    st.session_state.assessment_csv = None

if "assessment_filename" not in st.session_state:
    st.session_state.assessment_filename = None

if "inventory_df" not in st.session_state:
    st.session_state.inventory_df = None


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.markdown(
        "## Fabric Migration AI"
    )

    st.caption(
        "Enterprise workload assessment"
    )

    st.divider()


    st.markdown(
        "### Assessment flow"
    )


    st.markdown(
        """
**1. Upload**  
One or more migration inventory CSV files

**2. Consolidate**  
Valid files are combined into one batch

**3. ETL & Standardize**  
n8n cleans and normalizes workload data

**4. Ground**  
FAISS retrieves Microsoft migration guidance

**5. Assess**  
GPT generates structured recommendations

**6. Act**  
High-risk workloads trigger Slack alerts

**7. Report**  
Review and download consolidated results
"""
    )


    st.divider()


    st.markdown(
        "### Input requirements"
    )


    st.caption(
        "Each file must use the same "
        "Fabric migration inventory structure."
    )


    with st.expander(
        "Required columns"
    ):

        for column in REQUIRED_COLUMNS:

            st.code(
                column,
                language=None,
            )


    st.divider()


    st.markdown(
        "### Scope"
    )


    st.info(
        "This assessment engine currently targets "
        "Microsoft Fabric migrations. "
        "Other migration types require an appropriate "
        "knowledge base and assessment model."
    )


    st.divider()


    st.markdown(
        "### Governance"
    )


    st.info(
        "AI recommendations are advisory. "
        "Architecture, security, cost, performance "
        "and compliance decisions should be reviewed "
        "by qualified engineers."
    )


# =========================================================
# Hero
# =========================================================

html(
    '<div class="hero">'
    '<div class="hero-eyebrow">'
    'Enterprise Data Modernization'
    '</div>'
    '<div class="hero-title">'
    'AI-Powered Fabric Migration Assessment Platform'
    '</div>'
    '<div class="hero-subtitle">'
    'Assess migration workloads at scale using automated ETL, '
    'retrieval-augmented generation and Microsoft Fabric guidance. '
    'Upload one or more migration inventories, standardize raw data, '
    'identify migration risks, generate grounded recommendations, '
    'escalate critical workloads and produce a consolidated assessment report.'
    '</div>'
    '<div class="hero-status">'
    'Multi-File Batch Assessment '
    '&nbsp;•&nbsp; Automated ETL '
    '&nbsp;•&nbsp; RAG Grounded '
    '&nbsp;•&nbsp; Risk Escalation'
    '</div>'
    '</div>'
)


# =========================================================
# Capabilities
# =========================================================

html(
    '<div class="section-kicker">'
    'Platform capabilities'
    '</div>'
)


html(
    '<div class="section-title">'
    'From raw migration inventory to actionable insight'
    '</div>'
)


html(
    '<div class="section-description">'
    'The platform combines data preparation, workflow automation, '
    'retrieval-augmented generation and operational alerting.'
    '</div>'
)


cap1, cap2, cap3, cap4, cap5 = (
    st.columns(5)
)


with cap1:

    html(
        '<div class="card">'
        '<div class="card-number">01</div>'
        '<div class="card-title">'
        'Multi-File Batch Intake'
        '</div>'
        '<div class="card-text">'
        'Upload one or more migration inventory CSV files and '
        'combine all valid workloads into a single assessment batch.'
        '</div>'
        '</div>'
    )


with cap2:

    html(
        '<div class="card">'
        '<div class="card-number">02</div>'
        '<div class="card-title">'
        'ETL & Data Standardization'
        '</div>'
        '<div class="card-text">'
        'n8n parses and cleans raw CSV data, standardizes source '
        'platform names and business criticality, normalizes '
        'dependencies, and prepares structured API records.'
        '</div>'
        '</div>'
    )


with cap3:

    html(
        '<div class="card">'
        '<div class="card-number">03</div>'
        '<div class="card-title">'
        'Grounded AI Assessment'
        '</div>'
        '<div class="card-text">'
        'FAISS retrieves relevant Microsoft migration guidance before '
        'GPT generates recommendations and migration risk assessments.'
        '</div>'
        '</div>'
    )


with cap4:

    html(
        '<div class="card">'
        '<div class="card-number">04</div>'
        '<div class="card-title">'
        'Risk Escalation'
        '</div>'
        '<div class="card-text">'
        'High-risk workloads are automatically identified, '
        'highlighted in the portal and routed to Slack.'
        '</div>'
        '</div>'
    )


with cap5:

    html(
        '<div class="card">'
        '<div class="card-number">05</div>'
        '<div class="card-title">'
        'Assessment Reporting'
        '</div>'
        '<div class="card-text">'
        'Review results directly in the portal and download '
        'one consolidated structured migration assessment report.'
        '</div>'
        '</div>'
    )


st.write("")


# =========================================================
# Technology Stack
# =========================================================

html(
    '<div class="section-kicker">'
    'Solution architecture'
    '</div>'
)


html(
    '<div class="section-title">'
    'Technology used'
    '</div>'
)


html(
    '<div class="architecture-card">'
    '<div class="architecture-text">'
    'Streamlit provides the enterprise-facing upload and reporting experience. '
    'n8n orchestrates multi-record processing and performs ETL cleaning and '
    'standardization before invoking the FastAPI assessment service. '
    'FAISS retrieves relevant Microsoft migration guidance, GPT generates '
    'grounded recommendations, Slack handles high-risk escalation, and the '
    'completed report is returned to the portal for review and download.'
    '</div>'
    '<div class="tech-row">'
    '<span class="tech-pill">Streamlit</span>'
    '<span class="tech-pill">n8n</span>'
    '<span class="tech-pill">ETL</span>'
    '<span class="tech-pill">FastAPI</span>'
    '<span class="tech-pill">FAISS</span>'
    '<span class="tech-pill">LangChain</span>'
    '<span class="tech-pill">RAG</span>'
    '<span class="tech-pill">GPT-4.1</span>'
    '<span class="tech-pill">OpenAI Embeddings</span>'
    '<span class="tech-pill">Microsoft Learn</span>'
    '<span class="tech-pill">Slack</span>'
    '</div>'
    '</div>'
)


st.write("")


# =========================================================
# Assessment Intake
# =========================================================

html(
    '<div class="section-kicker">'
    'Migration assessment'
    '</div>'
)


html(
    '<div class="section-title">'
    'Submit migration inventories'
    '</div>'
)


html(
    '<div class="upload-panel">'
    '<div class="upload-heading">'
    'Upload one or more CSV files'
    '</div>'
    '<div class="upload-copy">'
    'Each CSV must contain the same required migration inventory fields. '
    'The portal validates each file and combines valid workloads into a '
    'single batch. n8n then performs ETL cleaning and normalization before '
    'the records are submitted to the AI assessment API.'
    '</div>'
    '</div>'
)


uploaded_files = st.file_uploader(
    "Migration inventory CSV files",
    type=["csv"],
    accept_multiple_files=True,
    help=(
        "Select one or more Fabric migration "
        "inventory CSV files."
    ),
)


# =========================================================
# Multi-File Validation / Preview
# =========================================================

inventory_valid = False
combined_inventory_df = None
combined_inventory_bytes = None


if uploaded_files:

    (
        combined_inventory_df,
        valid_file_names,
        validation_errors,
    ) = combine_inventory_files(
        uploaded_files
    )


    st.session_state.inventory_df = (
        combined_inventory_df
    )


    valid_file_count = len(
        valid_file_names
    )

    total_file_count = len(
        uploaded_files
    )

    total_workload_count = len(
        combined_inventory_df
    )


    info1, info2, info3, info4 = (
        st.columns(4)
    )


    with info1:

        st.metric(
            "Files selected",
            total_file_count,
        )


    with info2:

        st.metric(
            "Valid files",
            valid_file_count,
        )


    with info3:

        st.metric(
            "Total workloads",
            total_workload_count,
        )


    with info4:

        detected_columns = (
            len(
                combined_inventory_df.columns
            )
            if not combined_inventory_df.empty
            else 0
        )

        st.metric(
            "Detected columns",
            detected_columns,
        )


    if validation_errors:

        st.error(
            "One or more files failed validation."
        )

        for validation_error in (
            validation_errors
        ):

            st.write(
                f"• {validation_error}"
            )


    if (
        valid_file_count > 0
        and not combined_inventory_df.empty
        and not validation_errors
    ):

        inventory_valid = True

        combined_inventory_bytes = (
            dataframe_to_csv_bytes(
                combined_inventory_df
            )
        )


        st.success(
            f"Validation passed for {valid_file_count} file(s). "
            f"{total_workload_count} workload(s) are ready "
            f"for automated ETL and assessment."
        )


        with st.expander(
            "Files included in this assessment",
            expanded=False,
        ):

            for file_name in (
                valid_file_names
            ):

                st.write(
                    f"✓ {file_name}"
                )


        with st.expander(
            "Preview consolidated migration inventory",
            expanded=True,
        ):

            st.dataframe(
                combined_inventory_df,
                use_container_width=True,
                hide_index=True,
            )


# =========================================================
# Run Assessment
# =========================================================

if uploaded_files:

    run_assessment = st.button(
        "Run Fabric Migration Assessment",
        type="primary",
        disabled=not inventory_valid,
    )


    if run_assessment:

        st.session_state.assessment_df = None
        st.session_state.assessment_csv = None
        st.session_state.assessment_filename = None


        with st.spinner(
            "Running ETL cleaning, retrieving Microsoft guidance, "
            "generating AI recommendations and evaluating migration risk..."
        ):

            try:

                files = {
                    "file": (
                        "combined_migration_inventory.csv",
                        combined_inventory_bytes,
                        "text/csv",
                    )
                }


                response = requests.post(
                    WEBHOOK_URL,
                    files=files,
                    timeout=300,
                )


                if response.status_code == 200:

                    result_bytes = (
                        response.content
                    )


                    assessment_df = (
                        parse_csv_bytes(
                            result_bytes
                        )
                    )


                    if assessment_df.empty:

                        st.error(
                            "The workflow completed but returned "
                            "an empty assessment report."
                        )


                    else:

                        st.session_state.assessment_df = (
                            assessment_df
                        )

                        st.session_state.assessment_csv = (
                            result_bytes
                        )

                        st.session_state.assessment_filename = (
                            "fabric_migration_assessments.csv"
                        )


                        st.success(
                            "ETL processing and migration assessment "
                            "completed successfully."
                        )


                else:

                    st.error(
                        "Assessment workflow failed. "
                        f"HTTP status: {response.status_code}"
                    )

                    st.code(
                        response.text
                    )


            except requests.exceptions.Timeout:

                st.error(
                    "The assessment exceeded the "
                    "five-minute request timeout."
                )


            except requests.exceptions.RequestException as exc:

                st.error(
                    "Unable to connect to the "
                    "assessment workflow."
                )

                st.code(
                    str(exc)
                )


            except Exception as exc:

                st.error(
                    "The workflow completed, but the "
                    "assessment response could not be processed."
                )

                st.code(
                    str(exc)
                )


# =========================================================
# Assessment Results
# =========================================================

assessment_df = (
    st.session_state.assessment_df
)


if (
    assessment_df is not None
    and not assessment_df.empty
):

    st.divider()


    html(
        '<div class="section-kicker">'
        'Executive results'
        '</div>'
    )


    html(
        '<div class="section-title">'
        'Migration assessment summary'
        '</div>'
    )


    html(
        '<div class="section-description">'
        'Portfolio-level view of migration risk and workloads '
        'requiring further architectural attention.'
        '</div>'
    )


    risk_series = (
        assessment_df["risk_level"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )


    total_workloads = len(
        assessment_df
    )


    high_count = int(
        (
            risk_series == "high"
        ).sum()
    )


    medium_count = int(
        (
            risk_series == "medium"
        ).sum()
    )


    low_count = int(
        (
            risk_series == "low"
        ).sum()
    )


    human_review_count = 0


    if (
        "human_review_required"
        in assessment_df.columns
    ):

        human_review_series = (
            assessment_df[
                "human_review_required"
            ]
            .astype(str)
            .str.strip()
            .str.lower()
        )


        human_review_count = int(
            human_review_series.isin(
                [
                    "true",
                    "1",
                    "yes",
                ]
            ).sum()
        )


    metric1, metric2, metric3, metric4, metric5 = (
        st.columns(5)
    )


    with metric1:

        html(
            '<div class="metric-card">'
            '<div class="metric-label">'
            'TOTAL WORKLOADS'
            '</div>'
            f'<div class="metric-value">'
            f'{total_workloads}'
            '</div>'
            '<div class="metric-note">'
            'Current assessment batch'
            '</div>'
            '</div>'
        )


    with metric2:

        html(
            '<div class="metric-card metric-high">'
            '<div class="metric-label">'
            'HIGH RISK'
            '</div>'
            f'<div class="metric-value">'
            f'{high_count}'
            '</div>'
            '<div class="metric-note">'
            'Escalated through Slack'
            '</div>'
            '</div>'
        )


    with metric3:

        html(
            '<div class="metric-card metric-medium">'
            '<div class="metric-label">'
            'MEDIUM RISK'
            '</div>'
            f'<div class="metric-value">'
            f'{medium_count}'
            '</div>'
            '<div class="metric-note">'
            'Migration planning required'
            '</div>'
            '</div>'
        )


    with metric4:

        html(
            '<div class="metric-card metric-low">'
            '<div class="metric-label">'
            'LOW RISK'
            '</div>'
            f'<div class="metric-value">'
            f'{low_count}'
            '</div>'
            '<div class="metric-note">'
            'Lower assessed concern'
            '</div>'
            '</div>'
        )


    with metric5:

        html(
            '<div class="metric-card metric-review">'
            '<div class="metric-label">'
            'HUMAN REVIEW'
            '</div>'
            f'<div class="metric-value">'
            f'{human_review_count}'
            '</div>'
            '<div class="metric-note">'
            'Manual validation flagged'
            '</div>'
            '</div>'
        )


    # =====================================================
    # High-Risk Escalation Banner
    # =====================================================

    if high_count > 0:

        high_projects = (
            assessment_df.loc[
                risk_series == "high",
                "project_id",
            ]
            .astype(str)
            .tolist()
        )


        high_project_text = (
            ", ".join(
                high_projects
            )
        )


        html(
            '<div class="high-risk-alert">'
            '<div class="high-risk-alert-title">'
            'High-Risk Migration Workload Detected'
            '</div>'
            '<div class="high-risk-alert-text">'
            f'{high_project_text} '
            'requires additional migration review. '
            'The workflow has automatically triggered '
            'a Slack escalation for the migration team.'
            '</div>'
            '</div>'
        )


    # =====================================================
    # Assessment Register
    # =====================================================

    st.write("")


    html(
        '<div class="section-kicker">'
        'Portfolio view'
        '</div>'
    )


    html(
        '<div class="section-title">'
        'Assessment register'
        '</div>'
    )


    html(
        '<div class="section-description">'
        'High-risk workloads are highlighted in red, '
        'medium-risk workloads in amber and '
        'low-risk workloads in green.'
        '</div>'
    )


    preferred_columns = [
        "project_id",
        "risk_level",
        "confidence",
        "recommended_fabric_area",
        "human_review_required",
    ]


    visible_columns = [
        column
        for column in preferred_columns
        if column in assessment_df.columns
    ]


    summary_df = (
        assessment_df[
            visible_columns
        ].copy()
    )


    if (
        "risk_level"
        in summary_df.columns
    ):

        summary_df[
            "_risk_sort"
        ] = summary_df[
            "risk_level"
        ].apply(
            risk_sort_value
        )


        summary_df = (
            summary_df
            .sort_values(
                "_risk_sort"
            )
            .drop(
                columns=[
                    "_risk_sort"
                ]
            )
        )


    styled_summary_df = (
        summary_df.style.apply(
            highlight_risk_rows,
            axis=1,
        )
    )


    st.dataframe(
        styled_summary_df,
        use_container_width=True,
        hide_index=True,
    )


    # =====================================================
    # Detailed Assessments
    # =====================================================

    st.write("")


    html(
        '<div class="section-kicker">'
        'Workload analysis'
        '</div>'
    )


    html(
        '<div class="section-title">'
        'Detailed migration assessments'
        '</div>'
    )


    html(
        '<div class="section-description">'
        'Review the recommended Fabric area, assessment rationale, '
        'migration risks, considerations and grounding sources.'
        '</div>'
    )


    sorted_assessments = (
        assessment_df.copy()
    )


    sorted_assessments[
        "_risk_sort"
    ] = sorted_assessments[
        "risk_level"
    ].apply(
        risk_sort_value
    )


    sorted_assessments = (
        sorted_assessments
        .sort_values(
            "_risk_sort"
        )
        .drop(
            columns=[
                "_risk_sort"
            ]
        )
    )


    for _, row in (
        sorted_assessments.iterrows()
    ):

        project_id = clean_cell(
            row.get(
                "project_id"
            )
        )


        risk_level = clean_cell(
            row.get(
                "risk_level"
            )
        )


        confidence = clean_cell(
            row.get(
                "confidence"
            )
        )


        recommended_area = clean_cell(
            row.get(
                "recommended_fabric_area"
            )
        )


        human_review = clean_cell(
            row.get(
                "human_review_required"
            )
        )


        reason = clean_cell(
            row.get(
                "reason"
            )
        )


        with st.expander(
            f"{project_id}  •  {risk_level} Risk",
            expanded=(
                risk_level.lower()
                == "high"
            ),
        ):

            html(
                risk_badge(
                    risk_level
                )
            )


            st.write("")


            html(
                '<div class="detail-grid">'
                '<div class="detail-box">'
                '<div class="detail-label">'
                'Project'
                '</div>'
                f'<div class="detail-value">'
                f'{project_id}'
                '</div>'
                '</div>'
                '<div class="detail-box">'
                '<div class="detail-label">'
                'Confidence'
                '</div>'
                f'<div class="detail-value">'
                f'{confidence}'
                '</div>'
                '</div>'
                '<div class="detail-box">'
                '<div class="detail-label">'
                'Human Review'
                '</div>'
                f'<div class="detail-value">'
                f'{human_review}'
                '</div>'
                '</div>'
                '</div>'
            )


            st.markdown(
                "#### Recommended Fabric Area"
            )


            st.write(
                recommended_area
            )


            st.markdown(
                "#### Assessment Rationale"
            )


            st.write(
                reason
            )


            if (
                "key_risks"
                in assessment_df.columns
            ):

                risks = clean_collection(
                    row.get(
                        "key_risks"
                    )
                )


                if risks:

                    st.markdown(
                        "#### Key Risks"
                    )


                    for risk in risks:

                        st.markdown(
                            f"- {risk}"
                        )


            if (
                "migration_considerations"
                in assessment_df.columns
            ):

                considerations = (
                    clean_collection(
                        row.get(
                            "migration_considerations"
                        )
                    )
                )


                if considerations:

                    st.markdown(
                        "#### Migration Considerations"
                    )


                    for item in (
                        considerations
                    ):

                        st.markdown(
                            f"- {item}"
                        )


            if (
                "sources_used"
                in assessment_df.columns
            ):

                sources = (
                    clean_collection(
                        row.get(
                            "sources_used"
                        )
                    )
                )


                if sources:

                    st.markdown(
                        "#### Grounding Sources"
                    )


                    for source in sources:

                        st.markdown(
                            f"- {source}"
                        )


    # =====================================================
    # Download
    # =====================================================

    st.write("")


    html(
        '<div class="section-kicker">'
        'Reporting'
        '</div>'
    )


    html(
        '<div class="section-title">'
        'Download assessment report'
        '</div>'
    )


    html(
        '<div class="section-description">'
        'The download becomes available after the '
        'assessment workflow completes successfully.'
        '</div>'
    )


    download1, download2 = (
        st.columns(
            [1, 2]
        )
    )


    with download1:

        st.download_button(
            label="Download Assessment CSV",
            data=(
                st.session_state
                .assessment_csv
            ),
            file_name=(
                st.session_state
                .assessment_filename
            ),
            mime="text/csv",
            type="primary",
        )


    with download2:

        html(
            '<div class="download-note">'
            'This consolidated report contains the complete '
            'AI-generated assessment for all workloads submitted '
            'in the current batch.'
            '</div>'
        )


# =========================================================
# No Results Yet
# =========================================================

else:

    if uploaded_files:

        st.write("")

        html(
            '<div class="download-note">'
            '<strong>Assessment report:</strong> '
            'The Download Assessment CSV option will appear here '
            'after the assessment completes successfully.'
            '</div>'
        )


# =========================================================
# Governance
# =========================================================

st.write("")

st.divider()


html(
    '<div class="section-kicker">'
    'Governance'
    '</div>'
)


html(
    '<div class="section-title">'
    'Responsible use of AI-generated assessments'
    '</div>'
)


gov1, gov2, gov3 = (
    st.columns(3)
)


with gov1:

    html(
        '<div class="card">'
        '<div class="card-title">'
        'AI-assisted, not autonomous'
        '</div>'
        '<div class="card-text">'
        'The platform supports migration planning but does not replace '
        'architecture, security, networking, performance, cost or '
        'compliance review.'
        '</div>'
        '</div>'
    )


with gov2:

    html(
        '<div class="card">'
        '<div class="card-title">'
        'Grounded recommendations'
        '</div>'
        '<div class="card-text">'
        'The model receives retrieved Microsoft migration guidance before '
        'producing each recommendation, reducing reliance on model memory alone.'
        '</div>'
        '</div>'
    )


with gov3:

    html(
        '<div class="card">'
        '<div class="card-title">'
        'Human review remains essential'
        '</div>'
        '<div class="card-text">'
        'LLM assessments may vary between executions. High-impact migrations '
        'should be validated by a qualified migration architect.'
        '</div>'
        '</div>'
    )


# =========================================================
# Footer
# =========================================================

html(
    '<div class="enterprise-footer">'
    '<strong>'
    'AI-Powered Fabric Migration Assessment Platform'
    '</strong>'
    '<br>'
    'Streamlit • n8n • ETL • FastAPI • FAISS • LangChain • RAG • '
    'OpenAI • Microsoft Learn • Slack'
    '<br>'
    'Human-triggered, end-to-end automated AI migration assessment workflow'
    '</div>'
)