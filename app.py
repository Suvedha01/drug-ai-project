import streamlit as st
import pandas as pd
import joblib
import requests

st.set_page_config(page_title="LigandLogic", layout="wide")

# =========================
# 🎨 CLEAN UI
# =========================
st.markdown("""
<style>
.stApp {
    background: #002e5d;
    color: white;
    font-family: 'Poppins', sans-serif;
}

.title {
    text-align:center;
    font-size:42px;
    font-weight:700;
    color:#fbd786;
}

.tagline {
    text-align:center;
    font-size:14px;
    font-style:italic;
    color:#d1d5db;
    margin-bottom:20px;
}

.card {
    background: rgba(255,255,255,0.08);
    padding:20px;
    border-radius:12px;
    margin-top:15px;
}

input {
    background:#0b3d91 !important;
    color:white !important;
    border-radius:10px !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg,#ff4e50,#f9d423);
    color:white;
    border-radius:10px;
    height:3em;
    font-weight:600;
}

/* Result */
.result {
    text-align:center;
    font-size:26px;
    font-weight:700;
    padding:12px;
    border-radius:10px;
    margin-top:15px;
}

.good { background:#22c55e; }
.mid { background:#facc15; color:black; }
.bad { background:#ef4444; }

.metric {
    font-size:22px;
    font-weight:600;
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
# FEATURE ORDER (IMPORTANT)
# =========================
feature_order = [
 'MolWt','MolLogP','MolMR','HeavyAtomCount','NumHAcceptors',
 'NumHDonors','NumHeteroatoms','NumRotatableBonds',
 'NumValenceElectrons','NumAromaticRings','NumSaturatedRings',
 'NumAliphaticRings','RingCount','TPSA','LabuteASA',
 'BalabanJ','BertzCT'
]

# =========================
# GET PROPERTIES FROM API
# =========================
def get_properties(smiles):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount/JSON"
    
    try:
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            return None

        data = res.json()
        props = data['PropertyTable']['Properties'][0]

        return {
            'MolWt': float(props.get('MolecularWeight', 0)),
            'MolLogP': float(props.get('XLogP', 0) or 0),
            'NumHDonors': float(props.get('HBondDonorCount', 0)),
            'NumHAcceptors': float(props.get('HBondAcceptorCount', 0))
        }
    except:
        return None

# =========================
# INPUT
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
smiles = st.text_input("Enter SMILES", placeholder="e.g. CCO")
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ACTION
# =========================
if st.button("Analyze Molecule"):

    if not smiles:
        st.error("Please enter SMILES")
        st.stop()

    props = get_properties(smiles)

    if props is None:
        st.error("Could not fetch molecule data (try another SMILES)")
        st.stop()

    # =========================
    # BUILD FEATURES (CORRECT)
    # =========================
    features = pd.DataFrame([{
        'MolWt': props['MolWt'],
        'MolLogP': props['MolLogP'],
        'MolMR': 0.0,
        'HeavyAtomCount': 0.0,
        'NumHAcceptors': props['NumHAcceptors'],
        'NumHDonors': props['NumHDonors'],
        'NumHeteroatoms': 0.0,
        'NumRotatableBonds': 0.0,
        'NumValenceElectrons': 0.0,
        'NumAromaticRings': 0.0,
        'NumSaturatedRings': 0.0,
        'NumAliphaticRings': 0.0,
        'RingCount': 0.0,
        'TPSA': 0.0,
        'LabuteASA': 0.0,
        'BalabanJ': 0.0,
        'BertzCT': 0.0
    }])

    features = features[feature_order].astype(float)

    # =========================
    # PREDICT
    # =========================
    try:
        pred = model.predict(features)[0]
    except Exception as e:
        st.error("Model prediction failed ❌")
        st.write(features)
        st.stop()

    score = float((pred + 10) / 10)
    score = max(0, min(score, 1))

    # =========================
    # DECISION
    # =========================
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

    st.subheader("Extracted Molecular Properties")
    st.write(props)
