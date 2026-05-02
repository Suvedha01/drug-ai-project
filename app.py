import streamlit as st
import pandas as pd
import joblib
import requests

st.set_page_config(page_title="LigandLogic", layout="wide")

# =========================
# 🎨 UI STYLE (CLEAN + DARK)
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #0b1f3a, #002e5d);
    color: #EAEAEA;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 48px;
    font-weight: 700;
    color: #fbd786;
}

/* TAGLINE */
.tagline {
    text-align: center;
    font-size: 16px;
    font-style: italic;
    color: #cbd5e1;
    margin-bottom: 25px;
}

/* INPUT */
input {
    background-color: #1e3a5f !important;
    color: white !important;
    border-radius: 10px !important;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#ff4e50,#f9d423);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: 600;
}

/* RESULT BOX */
.result {
    text-align: center;
    font-size: 26px;
    font-weight: 700;
    padding: 15px;
    border-radius: 12px;
    margin-top: 20px;
}

.good { background: #22c55e; }
.mid { background: #facc15; color: black; }
.bad { background: #ef4444; }

/* METRICS */
.metric {
    font-size: 24px;
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
# PUBCHEM API FUNCTION
# =========================
def get_properties(smiles):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount/JSON"
    
    try:
        res = requests.get(url)
        data = res.json()
        props = data['PropertyTable']['Properties'][0]

        return {
            'MolWt': props.get('MolecularWeight', 0),
            'MolLogP': props.get('XLogP', 0) or 0,
            'NumHDonors': props.get('HBondDonorCount', 0),
            'NumHAcceptors': props.get('HBondAcceptorCount', 0)
        }
    except:
        return None

# =========================
# INPUT
# =========================
smiles = st.text_input("Enter SMILES", placeholder="e.g. CC(=O)OC1=CC=CC=C1C(=O)O")

# =========================
# REQUIRED MODEL FEATURES
# =========================
required_cols = [
 'MolWt','MolLogP','MolMR','HeavyAtomCount',
 'NumHAcceptors','NumHDonors','NumHeteroatoms',
 'NumRotatableBonds','NumValenceElectrons',
 'NumAromaticRings','NumSaturatedRings',
 'NumAliphaticRings','RingCount','TPSA',
 'LabuteASA','BalabanJ','BertzCT'
]

# =========================
# PREDICTION
# =========================
if st.button("Analyze Molecule"):

    props = get_properties(smiles)

    if props is None:
        st.error("❌ Invalid SMILES or API failed")
        st.stop()

    # =========================
    # BUILD FEATURE VECTOR CORRECTLY
    # =========================
    features = {}

    # Fill real values
    features['MolWt'] = float(props['MolWt'])
    features['MolLogP'] = float(props['MolLogP'])
    features['NumHDonors'] = float(props['NumHDonors'])
    features['NumHAcceptors'] = float(props['NumHAcceptors'])

    # Fill missing columns with 0
    for col in required_cols:
        if col not in features:
            features[col] = 0.0

    # Convert properly
    features_df = pd.DataFrame([[features[col] for col in required_cols]], columns=required_cols)
    features_df = features_df.astype(float)

    # =========================
    # MODEL PREDICTION
    # =========================
    pred = model.predict(features_df)[0]

    score = float((pred + 10) / 10)
    score = max(0.0, min(score, 1.0))

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
    col1.markdown(f'<div class="metric">AI Score: {score:.2f}</div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric">Confidence: {score*100:.1f}%</div>', unsafe_allow_html=True)

    st.progress(score)

    st.subheader("Extracted Molecular Properties")
    st.write(props)
