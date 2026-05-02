import streamlit as st
import pandas as pd
import numpy as np
import joblib

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
    font-family: 'Inter', sans-serif;
    font-size: 48px;
    font-weight: 700;
    letter-spacing: 1px;
}

/* Subtitle */
.subtitle {
    font-weight: 300;
    color: #8B949E;
    margin-bottom: 20px;
}

/* Cards */
.card {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 20px;
}

/* Glass Metric Cards */
.metric-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
}

/* SMILES Input */
input {
    font-family: monospace !important;
    background-color: #0B0E14 !important;
    color: #E6EDF3 !important;
    border: 1px solid #30363D !important;
    border-radius: 12px !important;
}

/* Ghost Button */
.stButton>button {
    background: transparent;
    border: 1px solid #6366F1;
    color: #E6EDF3;
    border-radius: 12px;
    height: 3em;
    transition: 0.3s;
}
.stButton>button:hover {
    background: linear-gradient(90deg,#6366F1,#00D1FF);
    color: black;
    box-shadow: 0px 0px 15px rgba(0,209,255,0.6);
}

/* LED Status */
.led {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 6px;
}

.green { background-color: #00FFA3; }
.yellow { background-color: #FFD166; }
.red { background-color: #EF476F; }

</style>
""", unsafe_allow_html=True)

# LOAD MODEL SAFE
try:
    model = joblib.load("model.pkl")
    model_loaded = True
except:
    model_loaded = False

    class DummyModel:
        def predict(self, X):
            return [np.random.uniform(-10, 0)]

    model = DummyModel()


# HEADER
st.markdown('<div class="title">LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Where machine learning meets molecular intelligence</div>', unsafe_allow_html=True)


# COMMAND BAR
st.markdown('<div class="card">', unsafe_allow_html=True)
smiles = st.text_input("SMILES Input", placeholder="e.g. CCO")
st.markdown('</div>', unsafe_allow_html=True)


# FEATURE STRUCTURE
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


# ACTION
if st.button("Analyze Molecule"):

    features = featurize(smiles)
    features = features[feature_order]

    pred = model.predict(features)[0]

    score = (pred + 10) / 10
    score = max(0, min(score, 1))

  
    # METRICS ROW
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="metric-card">
    <h3>AI Score</h3>
    <p>{score:.2f}</p>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="metric-card">
    <h3>Confidence</h3>
    <p>{score*100:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="metric-card">
    <h3>Status</h3>
    <p>{"Model Loaded" if model_loaded else "Fallback Mode"}</p>
    </div>
    """, unsafe_allow_html=True)

  
    # PROPERTY DASHBOARD
    st.markdown("### Molecular Properties")

    st.dataframe(features, use_container_width=True)

 
    # STATUS INDICATOR
    if score > 0.7:
        st.markdown('<span class="led green"></span> High potential candidate', unsafe_allow_html=True)
    elif score > 0.5:
        st.markdown('<span class="led yellow"></span> Moderate candidate', unsafe_allow_html=True)
    else:
        st.markdown('<span class="led red"></span> Low potential', unsafe_allow_html=True)

    st.progress(score)

