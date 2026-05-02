import streamlit as st
import joblib
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

# page config
st.set_page_config(page_title="Drug AI System", layout="wide")

# styling
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# title
st.title("🧬 AI Drug Candidate Prioritization System")
st.markdown("### Predict drug candidates using AI")

# load model
model = joblib.load("model.pkl")

# input
smiles = st.text_input("Enter SMILES (e.g., CCO)")

# feature function
def featurize(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        return pd.DataFrame([{
            'MolWt': Descriptors.MolWt(mol),
            'MolLogP': Descriptors.MolLogP(mol),
            'TPSA': Descriptors.TPSA(mol),
            'NumHDonors': Descriptors.NumHDonors(mol),
            'NumHAcceptors': Descriptors.NumHAcceptors(mol)
        }])
    return None

# prediction
if st.button("🚀 Predict"):
    features = featurize(smiles)

    if features is not None:
        pred = model.predict(features)[0]

        st.success(f"Predicted Score: {pred:.3f}")

        if pred > 0.7:
            st.info("✅ High potential drug candidate")
        else:
            st.warning("⚠️ Moderate candidate")
    else:
        st.error("Invalid SMILES")

# footer
st.markdown("---")
st.markdown("Built with ❤️ using AI & Bioinformatics")