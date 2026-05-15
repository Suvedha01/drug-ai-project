import streamlit as st
import requests
import pandas as pd

# PAGE CONFIG
st.set_page_config(
    page_title="BioBound",
    page_icon="🧬",
    layout="centered"
)

# TECH-BIO UI
st.markdown("""
<style>

/* Main Background */
.stApp{
    background:
    radial-gradient(circle at top left, rgba(0,255,255,0.10), transparent 30%),
    radial-gradient(circle at bottom right, rgba(123,97,255,0.15), transparent 30%),
    linear-gradient(135deg,#06121f,#0b1f33,#071522);
    color:#EAF2FF;
}

/* Remove Streamlit default padding */
.block-container{
    padding-top:2rem;
}

/* Title */
.title{
    text-align:center;
    font-size:58px;
    font-weight:800;
    letter-spacing:-1px;
    margin-bottom:5px;

    background: linear-gradient(90deg,#7DF9FF,#7B61FF,#00D4FF);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;

    text-shadow:0 0 25px rgba(0,212,255,0.25);
}

/* Tagline */
.tagline{
    text-align:center;
    font-size:17px;
    color:#A8C1E8;
    font-style:italic;
    margin-bottom:28px;
    letter-spacing:0.5px;
}

/* Input */
input{
    background:rgba(255,255,255,0.06)!important;
    color:white!important;

    border-radius:14px!important;
    border:1px solid rgba(125,249,255,0.20)!important;

    font-family:monospace!important;
}

/* Button */
.stButton>button{
    width:100%;

    background:linear-gradient(90deg,#00D4FF,#7B61FF);

    color:white;
    border:none;

    border-radius:14px;

    padding:14px;

    font-size:16px;
    font-weight:700;

    transition:0.3s ease;

    box-shadow:0 0 18px rgba(0,212,255,0.35);
}

.stButton>button:hover{
    transform:translateY(-2px);
    box-shadow:0 0 28px rgba(0,212,255,0.55);
}

/* Result Box */
.result{
    text-align:center;

    font-size:30px;
    font-weight:800;

    padding:18px;
    margin-top:25px;

    border-radius:18px;
}

.good{
    background:rgba(0,255,163,0.12);
    color:#00FFA3;
    border:1px solid rgba(0,255,163,0.25);
}

.mid{
    background:rgba(255,209,102,0.12);
    color:#FFD166;
    border:1px solid rgba(255,209,102,0.25);
}

.bad{
    background:rgba(255,107,107,0.12);
    color:#FF6B6B;
    border:1px solid rgba(255,107,107,0.25);
}

/* Metric Cards */
.metric-card{
    background:rgba(255,255,255,0.05);

    border:1px solid rgba(255,255,255,0.08);

    padding:18px;
    border-radius:18px;

    text-align:center;

    margin-top:12px;
}

.metric-title{
    font-size:14px;
    color:#9BB4D3;
}

.metric-value{
    font-size:28px;
    font-weight:700;
    margin-top:6px;

    background:linear-gradient(90deg,#7DF9FF,#7B61FF);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

/* Table */
[data-testid="stDataFrame"]{
    border-radius:16px;
    overflow:hidden;
}

/* Divider */
.divider{
    height:1px;
    margin:25px 0;

    background:linear-gradient(
    90deg,
    transparent,
    rgba(125,249,255,0.45),
    transparent
    );
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================
st.markdown(
    '<div class="title">🧬BIOBOUND</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="tagline">where machine learning meets molecular intelligence</div>',
    unsafe_allow_html=True
)

# =========================================
# MAIN CARD
# =========================================
st.markdown('<div class="card">', unsafe_allow_html=True)

smiles = st.text_input(
    "Enter SMILES",
    placeholder="e.g. CC(=O)OC1=CC=CC=C1C(=O)O"
)

# =========================================
# PUBCHEM FUNCTION
# =========================================
def get_properties(smiles):

    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,TPSA/JSON"

        response = requests.get(url, timeout=10)

        data = response.json()

        props = data["PropertyTable"]["Properties"][0]

        return {
            "Molecular Weight": float(props.get("MolecularWeight", 0) or 0),
            "LogP": float(props.get("XLogP", 0) or 0),
            "H Donors": float(props.get("HBondDonorCount", 0) or 0),
            "H Acceptors": float(props.get("HBondAcceptorCount", 0) or 0),
            "TPSA": float(props.get("TPSA", 0) or 0)
        }

    except:
        return None

# =========================================
# ANALYSIS
# =========================================
if st.button("Analyze Molecule"):

    if not smiles:
        st.error("Please enter a SMILES string")
        st.stop()

    props = get_properties(smiles)

    if props is None:
        st.error("Invalid SMILES or PubChem API error")
        st.stop()

    # =========================================
    # QED-INSPIRED CONTINUOUS SCORING
    # =========================================
    score = 1.0

    score -= abs(props["Molecular Weight"] - 350) / 1000
    score -= abs(props["LogP"] - 2.5) / 10
    score -= abs(props["TPSA"] - 75) / 300

    if props["H Donors"] > 6:
        score -= 0.1

    if props["H Acceptors"] > 12:
        score -= 0.1

    score = max(0.0, min(score, 1.0))

    # =========================================
    # THRESHOLDS
    # =========================================
    if score >= 0.60:
        decision = "DRUG-LIKE"
        cls = "good"

    elif score >= 0.35:
        decision = "MODERATE"
        cls = "mid"

    else:
        decision = "NOT DRUG-LIKE"
        cls = "bad"

    # =========================================
    # RESULT
    # =========================================
    st.markdown(
        f'<div class="result {cls}">{decision}</div>',
        unsafe_allow_html=True
    )

    st.progress(score)

    # =========================================
    # METRICS
    # =========================================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Drug-Likeness Score</div>
                <div class="metric-value">{score:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Confidence</div>
                <div class="metric-value">{score*100:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.subheader("Molecular Properties")

    df = pd.DataFrame([props])

    st.dataframe(df, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
