import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="LigandLogic", layout="wide")

# ===== BASIC CHECK ====
st.write("App started successfully")

# ===== TEMP MODEL (SAFE) =====
class DummyModel:
    def predict(self, X):
        return [np.random.uniform(-10, 0)]

model = DummyModel()

# ===== HEADER =====
st.title("LigandLogic")
st.caption("Where machine learning meets molecular intelligence")

# ===== INPUT =====
smiles = st.text_input("Enter SMILES", placeholder="e.g. CCO")

# ===== FEATURES =====
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

# ===== ACTION =====
if st.button("Analyze"):

    st.write("Running analysis...")

    features = featurize(smiles)
    features = features[feature_order]

    pred = model.predict(features)[0]

    # normalize score
    score = (pred + 10) / 10
    score = max(0, min(score, 1))

    # output
    st.success(f"Score: {score:.2f}")
    st.progress(score)

    if score > 0.7:
        st.success("High potential drug candidate")
    elif score > 0.5:
        st.info("Moderate candidate")
    else:
        st.warning("Low potential")

st.markdown("---")
st.caption("LigandLogic • Stable Mode")
