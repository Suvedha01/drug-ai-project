import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="LigandLogic", layout="wide")

# =========================
# 🎨 CUSTOM UI STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background: #002e5d;
    color: white;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg,#ff4e50,#f9d423);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* TAGLINE */
.tagline {
    text-align: center;
    font-size: 16px;
    font-style: italic;
    color: #fbd786;
    margin-bottom: 20px;
}

/* SECTION HEAD */
.section {
    font-size: 22px;
    margin-top: 30px;
    font-weight: 600;
}

/* INPUT BOXES */
.stNumberInput input {
    background: linear-gradient(90deg,#554023,#c99846);
    color: white !important;
    border-radius: 10px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#ff512f,#dd2476);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
}

/* RESULT BOX */
.result {
    text-align: center;
    font-size: 26px;
    font-weight: 700;
    padding: 15px;
    border-radius: 10px;
    margin-top: 15px;
}

.good { background: linear-gradient(90deg,#fbd786,#f7797d); color: black; }
.mid { background: linear-gradient(90deg,#fbd3e9,#bb377d); color: white; }
.bad { background: linear-gradient(90deg,#ff512f,#dd2476); color: white; }

/* METRIC */
.metric {
    font-size: 28px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="title">LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">where machine learning meets molecular intelligence</div>', unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("model.pkl")

# =========================
# INPUT SECTION
# =========================
st.markdown('<div class="section">Enter Molecular Properties</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    MolWt = st.number_input("Molecular Weight", 0.0, 1000.0, 180.0)
    MolLogP = st.number_input("LogP", 0.0, 10.0, 2.0)
    TPSA = st.number_input("TPSA", 0.0, 200.0, 80.0)

with col2:
    NumHDonors = st.number_input("H Donors", 0, 10, 1)
    NumHAcceptors = st.number_input("H Acceptors", 0, 15, 3)
    HeavyAtomCount = st.number_input("Heavy Atom Count", 0, 100, 20)

# =========================
# PREDICTION
# =========================
if st.button("Analyze Molecule"):

    # MATCH MODEL FEATURES
    features = pd.DataFrame([{
        'MolWt': MolWt,
        'MolLogP': MolLogP,
        'MolMR': 0,
        'HeavyAtomCount': HeavyAtomCount,
        'NumHAcceptors': NumHAcceptors,
        'NumHDonors': NumHDonors,
        'NumHeteroatoms': 0,
        'NumRotatableBonds': 0,
        'NumValenceElectrons': 0,
        'NumAromaticRings': 0,
        'NumSaturatedRings': 0,
        'NumAliphaticRings': 0,
        'RingCount': 0,
        'TPSA': TPSA,
        'LabuteASA': 0,
        'BalabanJ': 0,
        'BertzCT': 0
    }])

    pred = model.predict(features)[0]

    score = float((pred + 10) / 10)
    score = max(0, min(score, 1))

    # DECISION
    if score >= 0.7:
        decision, cls = "DRUG-LIKE", "good"
    elif score >= 0.4:
        decision, cls = "MODERATE", "mid"
    else:
        decision, cls = "NOT DRUG-LIKE", "bad"

    # =========================
    # OUTPUT
    # =========================
    st.markdown(f'<div class="result {cls}">{decision}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.markdown(f'<div class="metric">{score:.2f}</div><p>AI Score</p>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric">{score*100:.1f}%</div><p>Confidence</p>', unsafe_allow_html=True)

    st.progress(score)
