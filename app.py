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

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600;800&family=Ubuntu:wght@500&display=swap');

.stApp {
    background: linear-gradient(135deg, #002e5d, #001a33);
    color: white;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(90deg, #fbd786, #ff4e50);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* TAGLINE */
.tagline {
    text-align: center;
    font-style: italic;
    font-size: 16px;
    color: #e5e7eb;
    margin-bottom: 25px;
}

/* INPUT */
input {
    background: rgba(255,255,255,0.1) !important;
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
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
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
st.markdown('<div class="title">LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">where machine learning meets molecular intelligence</div>', unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("model.pkl")

# =========================
# PUBCHEM FUNCTION
# =========================
def get_properties(smiles):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,TPSA/JSON"
    
    try:
        res = requests.get(url, timeout=10)
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
# ANALYZE
# =========================
if st.button("Analyze Molecule"):

    if not smiles:
        st.error("Enter a SMILES string first")
        st.stop()

    props = get_properties(smiles)

    if props is None:
        st.error("Failed to fetch molecule data ❌")
        st.stop()

    # =========================
    # FEATURE MATCHING
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
    pred = model.predict(features)[0]

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
    col1.markdown(f"**AI Score:** {score:.2f}")
    col2.markdown(f"**Confidence:** {score*100:.1f}%")

    st.progress(score)

    st.markdown("### Molecular Properties")
    st.write(props)
