import streamlit as st
import pandas as pd
import joblib
import requests

st.set_page_config(page_title="LigandLogic", layout="wide")

# ================= UI =================
st.markdown("""
<style>
.stApp { background: #002e5d; color: white; }
.title { text-align:center; font-size:46px; font-weight:700; color:#fbd786; }
.tagline { text-align:center; font-style:italic; color:#d1d5db; margin-bottom:20px; }

.stButton>button {
    background: linear-gradient(90deg,#ff4e50,#f9d423);
    color:white; border-radius:10px; height:3em;
}

.result { text-align:center; font-size:24px; font-weight:700; padding:12px; border-radius:10px; }
.good { background:#22c55e; }
.mid { background:#facc15; color:black; }
.bad { background:#ef4444; }

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">where machine learning meets molecular intelligence</div>', unsafe_allow_html=True)

# ================= LOAD MODEL =================
model = joblib.load("model.pkl")

# ================= FUNCTION: GET DATA FROM PUBCHEM =================
def get_properties(smiles):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount/JSON"
    
    try:
        res = requests.get(url)
        data = res.json()

        props = data['PropertyTable']['Properties'][0]

        return {
            'MolWt': props.get('MolecularWeight', 0),
            'MolLogP': props.get('XLogP', 0),
            'NumHDonors': props.get('HBondDonorCount', 0),
            'NumHAcceptors': props.get('HBondAcceptorCount', 0)
        }

    except:
        return None

# ================= INPUT =================
smiles = st.text_input("Enter SMILES", placeholder="e.g. CCO")

# ================= ACTION =================
if st.button("Analyze Molecule"):

    props = get_properties(smiles)

    if props is None:
        st.error("Invalid SMILES or API failed ❌")
        st.stop()

    # ================= FEATURE MATCH =================
    features = pd.DataFrame([{
        'MolWt': props['MolWt'],
        'MolLogP': props['MolLogP'],
        'MolMR': 0,
        'HeavyAtomCount': 0,
        'NumHAcceptors': props['NumHAcceptors'],
        'NumHDonors': props['NumHDonors'],
        'NumHeteroatoms': 0,
        'NumRotatableBonds': 0,
        'NumValenceElectrons': 0,
        'NumAromaticRings': 0,
        'NumSaturatedRings': 0,
        'NumAliphaticRings': 0,
        'RingCount': 0,
        'TPSA': 0,
        'LabuteASA': 0,
        'BalabanJ': 0,
        'BertzCT': 0
    }])

    # ================= PREDICT =================
    pred = model.predict(features)[0]

    score = float((pred + 10) / 10)
    score = max(0, min(score, 1))

    # ================= DECISION =================
    if score >= 0.7:
        decision, cls = "DRUG-LIKE", "good"
    elif score >= 0.4:
        decision, cls = "MODERATE", "mid"
    else:
        decision, cls = "NOT DRUG-LIKE", "bad"

    # ================= OUTPUT =================
    st.markdown(f'<div class="result {cls}">{decision}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.write(f"AI Score: {score:.2f}")
    col2.write(f"Confidence: {score*100:.1f}%")

    st.progress(score)

    st.subheader("Extracted Molecular Properties")
    st.write(props)
