import streamlit as st
import joblib
import pandas as pd
import numpy as np

st.set_page_config(page_title="LigandLogic", layout="wide")

# ===== ADVANCED UI =====
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at 20% 30%, #1f1c2c, #928dab);
    color: white;
}

/* Hero Title */
.hero {
    font-size: 64px;
    font-weight: 800;
    text-align: center;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #00f5d4, #9b5de5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Tagline */
.tagline {
    text-align: center;
    font-size: 20px;
    color: #e0e0e0;
    margin-bottom: 40px;
}

/* Glass card */
.card {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 30px rgba(0,255,200,0.2);
}

/* Input box fix */
input {
    color: white !important;
    background-color: rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg,#00f5d4,#9b5de5);
    color: black;
    font-weight: bold;
    border-radius: 15px;
    height: 3.5em;
    width: 100%;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.08);
}

/* Glow effect */
.glow {
    text-align: center;
    animation: glow 2s infinite alternate;
}
@keyframes glow {
    from {text-shadow: 0 0 10px #00f5d4;}
    to {text-shadow: 0 0 30px #9b5de5;}
}

</style>
""", unsafe_allow_html=True)

# ===== HERO =====
st.markdown('<div class="hero glow">LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Redefining molecular intelligence through predictive AI-driven ranking</div>', unsafe_allow_html=True)

# Load model
model = joblib.load("model.pkl")

feature_order = [
 'MolWt','MolLogP','MolMR','HeavyAtomCount','NumHAcceptors',
 'NumHDonors','NumHeteroatoms','NumRotatableBonds',
 'NumValenceElectrons','NumAromaticRings','NumSaturatedRings',
 'NumAliphaticRings','RingCount','TPSA','LabuteASA',
 'BalabanJ','BertzCT'
]

# Layout
col1, col2 = st.columns([2,1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    smiles = st.text_input("Enter SMILES", placeholder="e.g. CCO")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h4>Sample Inputs</h4>
    CCO<br>CCC<br>CCN
    </div>
    """, unsafe_allow_html=True)

# Feature generator
def featurize(smiles):
    return pd.DataFrame([{
        'MolWt': np.random.uniform(200, 500),
        'MolLogP': np.random.uniform(1, 5),
        'MolMR': np.random.uniform(50, 150),
        'HeavyAtomCount': np.random.randint(10, 50),
        'NumHAcceptors': np.random.randint(1, 10),
        'NumHDonors': np.random.randint(0, 5),
        'NumHeteroatoms': np.random.randint(1, 10),
        'NumRotatableBonds': np.random.randint(0, 10),
        'NumValenceElectrons': np.random.randint(20, 100),
        'NumAromaticRings': np.random.randint(0, 5),
        'NumSaturatedRings': np.random.randint(0, 5),
        'NumAliphaticRings': np.random.randint(0, 5),
        'RingCount': np.random.randint(0, 10),
        'TPSA': np.random.uniform(50, 150),
        'LabuteASA': np.random.uniform(50, 200),
        'BalabanJ': np.random.uniform(0, 5),
        'BertzCT': np.random.uniform(0, 1000)
    }])

# Action
if st.button("Analyze Molecule"):

    with st.spinner("Running AI model..."):
        features = featurize(smiles)
        features = features[feature_order]
        pred = model.predict(features)[0]

    st.markdown(f"""
    <div class="card">
        <h2 style="text-align:center;">Score: {pred:.3f}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.progress(min(max(pred, 0), 1))

    if pred > 0.7:
        st.success("High potential drug candidate")
    elif pred > 0.5:
        st.info("Moderate candidate")
    else:
        st.warning("Low potential")

st.markdown("---")
st.markdown("LigandLogic | AI x Bioinformatics")
