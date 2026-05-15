import streamlit as st
import requests
import pandas as pd

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="LigandLogic",
    layout="centered"
)

# =========================================
# PREMIUM UI
# =========================================
st.markdown("""
<style>

/* Background */
.stApp{
    background: linear-gradient(135deg,#f8fbff,#eef4ff);
    color:#111827;
}

/* Title */
.title{
    text-align:center;
    font-size:54px;
    font-weight:800;
    margin-top:10px;
    background: linear-gradient(90deg,#ff512f,#dd2476,#7b61ff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

/* Tagline */
.tagline{
    text-align:center;
    font-size:16px;
    color:#6b7280;
    font-style:italic;
    margin-bottom:20px;
}

/* Card */
.card{
    background:white;
    padding:25px;
    border-radius:18px;
    box-shadow:0 8px 30px rgba(0,0,0,0.08);
    margin-top:10px;
}

/* Input */
input{
    border-radius:12px !important;
}

/* Button */
.stButton>button{
    width:100%;
    border:none;
    border-radius:12px;
    padding:12px;
    font-size:16px;
    font-weight:700;
    color:white;
    background:linear-gradient(90deg,#ff512f,#f9d423);
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.02);
}

/* Result */
.result{
    text-align:center;
    font-size:28px;
    font-weight:800;
    padding:16px;
    border-radius:14px;
    margin-top:20px;
}

.good{
    background:#dcfce7;
    color:#166534;
}

.mid{
    background:#fef3c7;
    color:#92400e;
}

.bad{
    background:#fee2e2;
    color:#991b1b;
}

/* Metric cards */
.metric-card{
    background:white;
    padding:16px;
    border-radius:14px;
    text-align:center;
    box-shadow:0 4px 15px rgba(0,0,0,0.06);
}

.metric-title{
    font-size:14px;
    color:#6b7280;
}

.metric-value{
    font-size:24px;
    font-weight:700;
    margin-top:5px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================
st.markdown('<div class="title">🧬 LigandLogic</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="tagline">where machine learning meets molecular intelligence</div>',
    unsafe_allow_html=True
)

# =========================================
# INPUT CARD
# =========================================
st.markdown('<div class="card">', unsafe_allow_html=True)

smiles = st.text_input(
    "Enter SMILES",
    placeholder="e.g. CC(=O)OC1=CC=CC=C1C(=O)O"
)

# =========================================
# PUBCHEM API
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

    # Smooth penalty system
    score -= abs(props["Molecular Weight"] - 350) / 1000
    score -= abs(props["LogP"] - 2.5) / 10
    score -= abs(props["TPSA"] - 75) / 300

    if props["H Donors"] > 6:
        score -= 0.1

    if props["H Acceptors"] > 12:
        score -= 0.1

    # Clamp score
    score = max(0.0, min(score, 1.0))

    # =========================================
    # DECISION
    # =========================================
    if score >= 0.7:
        decision = "DRUG-LIKE"
        cls = "good"

    elif score >= 0.4:
        decision = "MODERATE"
        cls = "mid"

    else:
        decision = "NOT DRUG-LIKE"
        cls = "bad"

    # =========================================
    # RESULT DISPLAY
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

    st.markdown("### Molecular Properties")

    df = pd.DataFrame([props])

    st.dataframe(df, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
