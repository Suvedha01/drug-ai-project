import streamlit as st
import pandas as pd
import joblib
from rdkit import Chem
from rdkit.Chem import Descriptors

st.set_page_config(page_title="LigandLogic", layout="wide")

# =========================
# 🎨 CLEAN PROFESSIONAL UI
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: #e2e8f0;
}

/* Title */
.title {
    text-align: center;
    font-size: 44px;
    font-weight: 600;
    color: #f8fafc;
}

/* Tagline */
.tagline {
    text-align: center;
    font-size: 14px;
    font-style: italic;
    color: #94a3b8;
    margin-bottom: 30px;
}

/* Input */
input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 8px !important;
}

/* Button */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    height: 2.8em;
    font-weight: 500;
}

/* Result */
.result {
    text-align: center;
    font-size: 24px;
    font-weight: 600;
    padding: 12px;
    border-radius: 10px;
    margin-top: 20px;
}

.good { background: #16a34a; }
.mid { background: #eab308; color:black; }
.bad { background: #dc2626; }

/* Cards */
.card {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 10px;
    margin-top: 15px;
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
# RDKit FEATURE EXTRACTION
# =========================
def featurize(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    data = {
        'MolWt': Descriptors.MolWt(mol),
        'MolLogP': Descriptors.MolLogP(mol),
        'MolMR': Descriptors.MolMR(mol),
        'HeavyAtomCount': Descriptors.HeavyAtomCount(mol),
        'NumHAcceptors': Descriptors.NumHAcceptors(mol),
        'NumHDonors': Descriptors.NumHDonors(mol),
        'NumHeteroatoms': Descriptors.NumHeteroatoms(mol),
        'NumRotatableBonds': Descriptors.NumRotatableBonds(mol),
        'NumValenceElectrons': Descriptors.NumValenceElectrons(mol),
        'NumAromaticRings': Descriptors.NumAromaticRings(mol),
        'NumSaturatedRings': Descriptors.NumSaturatedRings(mol),
        'NumAliphaticRings': Descriptors.NumAliphaticRings(mol),
        'RingCount': Descriptors.RingCount(mol),
        'TPSA': Descriptors.TPSA(mol),
        'LabuteASA': Descriptors.LabuteASA(mol),
        'BalabanJ': Descriptors.BalabanJ(mol),
        'BertzCT': Descriptors.BertzCT(mol)
    }

    return pd.DataFrame([data])

# =========================
# INPUT
# =========================
smiles = st.text_input("Enter SMILES", placeholder="e.g. CC(=O)OC1=CC=CC=C1C(=O)O")

# =========================
# ACTION
# =========================
if st.button("Analyze Molecule"):

    features = featurize(smiles)

    if features is None:
        st.error("Invalid SMILES ❌")
        st.stop()

    # =========================
    # MODEL PREDICTION
    # =========================
    pred = model.predict(features)[0]

    score = float((pred + 10) / 10)
    score = max(0.0, min(score, 1.0))

    # =========================
    # DECISION
    # =========================
    if score >= 0.7:
        label, cls = "Drug-like", "good"
    elif score >= 0.4:
        label, cls = "Moderate", "mid"
    else:
        label, cls = "Not drug-like", "bad"

    # =========================
    # OUTPUT
    # =========================
    st.markdown(f'<div class="result {cls}">{label}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.metric("Score", f"{score:.2f}")
    col2.metric("Confidence", f"{score*100:.1f}%")

    st.progress(score)

    # =========================
    # CLEAN PROPERTY DISPLAY
    # =========================
    st.markdown("### Molecular Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mol Weight", f"{features['MolWt'][0]:.1f}")
    c2.metric("LogP", f"{features['MolLogP'][0]:.2f}")
    c3.metric("H Donors", int(features['NumHDonors'][0]))
    c4.metric("H Acceptors", int(features['NumHAcceptors'][0]))
