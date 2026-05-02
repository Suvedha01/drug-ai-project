import streamlit as st
import joblib
import pandas as pd
import numpy as np

st.set_page_config(page_title="LigandLogic", layout="wide")

st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0B0E14;
    color: #E6EDF3;
}

/* Title */
.title {
    font-size: 52px;
    font-weight: 700;
    letter-spacing: 1px;
    text-align: center;
    color: white;
    text-shadow: 0px 0px 15px rgba(0, 209, 255, 0.3);
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #8B949E;
    margin-bottom: 30px;
}

/* Cards */
.card {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 20px;
}

/* SMILES input */
textarea, input {
    background-color: #0B0E14 !important;
    color: #E6EDF3 !important;
    border: 1px solid #30363D !important;
    font-family: monospace !important;
    border-radius: 8px !important;
}

/* Button */
.stButton>button {
    background-color: #00D1FF;
    color: black;
    font-weight: 600;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.stButton>button:hover {
    box-shadow: 0px 0px 15px rgba(0, 209, 255, 0.6);
}

/* Sample chips */
.chip {
    display: inline-block;
    padding: 8px 12px;
    margin: 5px;
    border-radius: 8px;
    background-color: #21262D;
    border: 1px solid #30363D;
    cursor: pointer;
}
.chip:hover {
    background-color: #30363D;
}

/* Stats */
.stat {
    font-size: 20px;
    font-weight: 600;
    color: #00FFA3;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="title">LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-driven molecular prioritization for computational drug discovery</div>', unsafe_allow_html=True)


# LOAD MODEL
model = joblib.load("model.pkl")

feature_order = [
 'MolWt','MolLogP','MolMR','HeavyAtomCount','NumHAcceptors',
 'NumHDonors','NumHeteroatoms','NumRotatableBonds',
 'NumValenceElectrons','NumAromaticRings','NumSaturatedRings',
 'NumAliphaticRings','RingCount','TPSA','LabuteASA',
 'BalabanJ','BertzCT'
]


# LAYOUT
col_main, col_side = st.columns([3, 1.5])


# LEFT PANEL
with col_main:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    smiles = st.text_input("SMILES Input", placeholder="Enter molecule (e.g. CCO)")

    st.markdown("**Sample Molecules:**")

    # clickable chips (simulated)
    sample_list = ["CCO", "CCC", "CCN", "C1=CC=CC=C1"]

    selected_sample = None
    cols = st.columns(len(sample_list))
    for i, s in enumerate(sample_list):
        if cols[i].button(s):
            selected_sample = s

    if selected_sample:
        smiles = selected_sample

    st.markdown('</div>', unsafe_allow_html=True)


# RIGHT PANEL
with col_side:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### Prediction Stats")

    score_placeholder = st.empty()
    rank_placeholder = st.empty()

    st.markdown('</div>', unsafe_allow_html=True)


# FEATURE GENERATION
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


# ACTION BUTTON
if st.button("Analyze"):

    features = featurize(smiles)
    features = features[feature_order]

    pred = model.predict(features)[0]

    # Update stats panel
    score_placeholder.markdown(f'<div class="stat">Score: {pred:.3f}</div>', unsafe_allow_html=True)
    rank_placeholder.markdown(f'<div class="stat">Rank Confidence: {pred*100:.1f}%</div>', unsafe_allow_html=True)

    st.progress(min(max(pred, 0), 1))

# FOOTER
st.markdown("---")
st.markdown("LigandLogic • Computational Drug Discovery Interface")
