import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="LigandLogic", layout="centered")

# ---------------- UI ----------------
st.markdown("""
<style>
body { background-color:#ffffff; }
.title { text-align:center; font-size:40px; font-weight:bold; }
.tagline { text-align:center; font-style:italic; color:#555; margin-bottom:20px; }
.stButton>button {
    background: linear-gradient(90deg,#ff4e50,#f9d423);
    color:white;
    border-radius:8px;
}
.result {
    text-align:center;
    font-size:22px;
    font-weight:bold;
    padding:12px;
    border-radius:10px;
    margin-top:20px;
}
.good { background:#4ade80; }
.mid { background:#facc15; }
.bad { background:#f87171; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">where machine learning meets molecular intelligence</div>', unsafe_allow_html=True)

# ---------------- INPUT ----------------
smiles = st.text_input("Enter SMILES", placeholder="e.g. CC(=O)OC1=CC=CC=C1C(=O)O")

# ---------------- API ----------------
def get_data(smiles):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,TPSA/JSON"
        r = requests.get(url, timeout=5)
        data = r.json()
        p = data["PropertyTable"]["Properties"][0]
        return {
            "MolWt": p.get("MolecularWeight",0),
            "LogP": p.get("XLogP",0),
            "Donors": p.get("HBondDonorCount",0),
            "Acceptors": p.get("HBondAcceptorCount",0),
            "TPSA": p.get("TPSA",0)
        }
    except:
        return None

# ---------------- ANALYSIS ----------------
if st.button("Analyze"):

    if not smiles:
        st.error("Enter SMILES")
        st.stop()

    props = get_data(smiles)

    if props is None:
        st.error("Invalid SMILES or API error")
        st.stop()

    # Lipinski scoring
    score = 0

    if 180 <= props["MolWt"] <= 500:
        score += 1
    if 0 <= props["LogP"] <= 5:
        score += 1
    if props["Donors"] <= 5:
        score += 1
    if props["Acceptors"] <= 10:
        score += 1
    if 20 <= props["TPSA"] <= 140:
        score += 1

    final_score = score / 5

    # decision
    if final_score >= 0.8:
        decision, cls = "DRUG-LIKE", "good"
    elif final_score >= 0.5:
        decision, cls = "MODERATE", "mid"
    else:
        decision, cls = "NOT DRUG-LIKE", "bad"

    # ---------------- OUTPUT ----------------
    st.markdown(f'<div class="result {cls}">{decision}</div>', unsafe_allow_html=True)

    st.write(f"Score: {round(final_score,2)}")
    st.progress(final_score)

    st.write("### Properties")
    st.write(pd.DataFrame([props]))
