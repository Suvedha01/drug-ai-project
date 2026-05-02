import streamlit as st
from rdkit import Chem
from rdkit.Chem import Descriptors, QED
import pandas as pd

st.set_page_config(page_title="LigandLogic", layout="wide")

# =========================
# 🎨 CLEAN PROFESSIONAL UI
# =========================
st.markdown("""
<style>
body {
    background-color: #f8fafc;
}
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}
.tagline {
    text-align: center;
    font-style: italic;
    color: gray;
    margin-bottom: 20px;
}
.stButton>button {
    background: linear-gradient(90deg,#ff4e50,#f9d423);
    color: white;
    border-radius: 10px;
}
.result {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    padding: 15px;
    border-radius: 10px;
    margin-top: 20px;
}
.good { background-color: #4ade80; }
.mid { background-color: #facc15; }
.bad { background-color: #f87171; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">where machine learning meets molecular intelligence</div>', unsafe_allow_html=True)

# =========================
# INPUT
# =========================
smiles = st.text_input("Enter SMILES", placeholder="e.g. CC(=O)OC1=CC=CC=C1C(=O)O")

# =========================
# MAIN LOGIC
# =========================
if st.button("Analyze Molecule"):

    if not smiles:
        st.error("Enter SMILES first")
        st.stop()

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        st.error("Invalid SMILES")
        st.stop()

    # =========================
    # MOLECULAR DESCRIPTORS
    # =========================
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    donors = Descriptors.NumHDonors(mol)
    acceptors = Descriptors.NumHAcceptors(mol)
    tpsa = Descriptors.TPSA(mol)

    # =========================
    # QED SCORE (REAL LOGIC)
    # =========================
    qed_score = QED.qed(mol)

    # =========================
    # DECISION
    # =========================
    if qed_score >= 0.6:
        decision, cls = "DRUG-LIKE", "good"
    elif qed_score >= 0.4:
        decision, cls = "MODERATE", "mid"
    else:
        decision, cls = "NOT DRUG-LIKE", "bad"

    # =========================
    # OUTPUT
    # =========================
    st.markdown(f'<div class="result {cls}">{decision}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.write(f"QED Score: {qed_score:.2f}")
    col2.write(f"Confidence: {qed_score*100:.1f}%")

    st.progress(qed_score)

    st.write("### Molecular Properties")
    st.write(pd.DataFrame([{
        "Molecular Weight": round(mw,2),
        "LogP": round(logp,2),
        "H Donors": donors,
        "H Acceptors": acceptors,
        "TPSA": round(tpsa,2)
    }]))
