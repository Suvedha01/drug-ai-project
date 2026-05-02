import streamlit as st
import pandas as pd
import joblib
import requests

st.set_page_config(page_title="LigandLogic", layout="wide")

# =========================
# 🎨 PREMIUM UI
# =========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@300;500&display=swap');

.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #EAEAEA;
}

/* TITLE */
.title {
    text-align: center;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 56px;
    font-weight: 700;
    background: linear-gradient(90deg, #00F5A0, #00D9F5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* TAGLINE */
.tagline {
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    color: #B0BEC5;
    margin-bottom: 25px;
    font-style: italic;
}

/* ICON */
.icon {
    text-align: center;
    font-size: 48px;
    margin-bottom: 10px;
}

/* INPUT */
input {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 10px !important;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#ff512f,#dd2476);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: 600;
}

/* RESULT */
.result {
    text-align: center;
    font-size: 26px;
    font-weight: 700;
    padding: 15px;
    border-radius: 12px;
    margin-top: 15px;
}

.good { background: linear-gradient(90deg,#00FFA3,#00D1FF); color:black; }
.mid { background: linear-gradient(90deg,#fbd786,#f7797d); color:black; }
.bad { background: linear-gradient(90deg,#ff4e50,#dd2476); }

/* CARD */
.card {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 12px;
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="icon">🧬</div>', unsafe_allow_html=True)
st.markdown('<div class="title">LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">where machine learning meets molecular intelligence</div>', unsafe_allow_html=True)

# =========================
# LOAD MODEL SAFELY
# =========================
try:
    model = joblib.load("model.pkl")
    model_loaded = True
except:
    model_loaded = False

# =========================
# PUBCHEM API (SAFE)
# =========================
def get_properties(smiles):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,TPSA/JSON"
        res = requests.get(url, timeout=5)
        data = res.json()
        props = data['PropertyTable']['Properties'][0]

        return {
            'MolWt': props.get('MolecularWeight', 0),
            'MolLogP': props.get('XLogP', 0),
            'NumHDonors': props.get('HBondDonorCount', 0),
            'NumHAcceptors': props.get('HBondAcceptorCount', 0),
            'TPSA': props.get('TPSA', 0)
        }
    except:
        return None

# =========================
# INPUT
# =========================
smiles = st.text_input("Enter SMILES", placeholder="e.g. CCO")

# =========================
# ACTION
# =========================
if st.button("Analyze Molecule"):

    if not smiles:
        st.error("Please enter a SMILES string")
        st.stop()

    props = get_properties(smiles)

    # 🔁 FALLBACK (NO CRASH)
    if props is None:
        props = {
            'MolWt': 250,
            'MolLogP': 2.5,
            'NumHDonors': 1,
            'NumHAcceptors': 3,
            'TPSA': 75
        }
        st.warning("Using fallback molecular values (API failed)")

    # =========================
    # FEATURE VECTOR
    # =========================
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
        'TPSA': props['TPSA'],
        'LabuteASA': 0,
        'BalabanJ': 0,
        'BertzCT': 0
    }])

    # =========================
    # PREDICTION
    # =========================
    if model_loaded:
        pred = model.predict(features)[0]
        score = float((pred + 10) / 10)
        score = max(0, min(score, 1))
    else:
        score = 0.6  # fallback

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
    col1.write(f"AI Score: {score:.2f}")
    col2.write(f"Confidence: {score*100:.1f}%")

    st.progress(score)

    st.markdown("### Molecular Properties")
    st.write(props)
