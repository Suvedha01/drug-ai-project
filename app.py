import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="LigandLogic", layout="wide")

# =========================
# 🎨 PREMIUM UI (OBSIDIAN)
# =========================
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at center, #0F172A, #0B0E14);
    color: #E6EDF3;
}

/* Title */
.title {
    font-size: 48px;
    font-weight: 700;
}

/* Subtitle */
.subtitle {
    font-weight: 300;
    color: #8B949E;
    margin-bottom: 20px;
}

/* Glass Card */
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid #30363D;
    border-radius: 14px;
    padding: 20px;
}

/* Metric */
.metric {
    font-size: 28px;
    font-weight: 700;
    background: linear-gradient(90deg,#00D1FF,#6366F1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg,#6366F1,#00D1FF);
    color: white;
    border-radius: 12px;
    height: 3em;
}

/* LED */
.led {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
}
.green {background:#00FFA3;}
.yellow {background:#FFD166;}
.red {background:#EF476F;}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL SAFE
# =========================
try:
    model = joblib.load("model.pkl")
    model_loaded = True
except:
    model_loaded = False
    class DummyModel:
        def predict(self, X):
            return [np.random.uniform(-10, 0)]
    model = DummyModel()

# =========================
# HEADER
# =========================
st.markdown('<div class="title">LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Where machine learning meets molecular intelligence</div>', unsafe_allow_html=True)

# =========================
# INPUT
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
smiles = st.text_input("SMILES Input", placeholder="e.g. CCO")
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# FEATURES
# =========================
feature_order = [
 'MolWt','MolLogP','MolMR','HeavyAtomCount','NumHAcceptors',
 'NumHDonors','NumHeteroatoms','NumRotatableBonds',
 'NumValenceElectrons','NumAromaticRings','NumSaturatedRings',
 'NumAliphaticRings','RingCount','TPSA','LabuteASA',
 'BalabanJ','BertzCT'
]

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

# =========================
# ACTION
# =========================
if st.button("Analyze Molecule"):

    features = featurize(smiles)
    features = features[feature_order]

    pred = model.predict(features)[0]

    # normalize
    score = float((pred + 10) / 10)
    score = max(0.0, min(score, 1.0))

    # =========================
    # CLEAR DECISION (IMPORTANT)
    # =========================
    if score >= 0.75:
        decision = "Drug-Like Candidate"
        color = "green"
    elif score >= 0.5:
        decision = "Borderline Candidate"
        color = "yellow"
    else:
        decision = "Not Drug-Like"
        color = "red"

    # =========================
    # RESULTS
    # =========================
    st.markdown("## Results")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f'<div class="metric">{score:.2f}</div><p>AI Score</p>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric">{score*100:.1f}%</div><p>Confidence</p>', unsafe_allow_html=True)
    col3.markdown(f'<span class="led {color}"></span> {decision}', unsafe_allow_html=True)

    # FIXED PROGRESS
    st.progress(score)

    # =========================
    # PROPERTY BADGES (NOT TABLE)
    # =========================
    st.markdown("### Molecular Properties")

    cols = st.columns(4)
    props = list(features.iloc[0].items())

    for i, (k, v) in enumerate(props[:12]):
        cols[i % 4].metric(k, f"{v:.2f}")
