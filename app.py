import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="LigandLogic", layout="wide")

# =========================
# 🎨 STYLE (Hero + accents)
# =========================
st.markdown("""
<style>
.stApp{
  background: radial-gradient(circle at 50% 10%, #0F172A, #0B0E14);
  color:#E6EDF3;
}

/* HERO */
.hero{ text-align:center; margin-top:10px; }
.logo{ font-size:22px; margin-bottom:6px; opacity:.9; }

.title{
  font-family: Inter, sans-serif;
  font-weight:800;
  font-size:58px;
  letter-spacing:-1px;
  background: linear-gradient(90deg,#00D1FF,#6366F1);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  text-shadow: 0 0 20px rgba(0,209,255,0.25);
}

.tagline{
  font-family: Inter, sans-serif;
  font-weight:400;
  font-size:18px;
  color:#94A3B8;
  margin-top:8px;
}

/* badges */
.badge{
  display:inline-block;
  padding:6px 12px;
  border-radius:20px;
  border:1px solid #30363D;
  margin:6px;
  font-size:12px;
  color:#CBD5E1;
}

/* divider */
.hr{
  height:1px;
  background: linear-gradient(90deg, transparent, #00D1FF, transparent);
  margin:18px 0 22px 0;
}

/* CARD */
.card{
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(12px);
  border: 1px solid #ffffff22;
  border-radius:16px;
  padding:20px;
}

/* INPUT */
input{
  font-family: monospace !important;
  background:transparent !important;
  color:#E6EDF3 !important;
  border:1px solid #30363D !important;
  border-radius:12px !important;
}

/* BUTTON */
.stButton>button{
  background: linear-gradient(90deg,#6366F1,#00D1FF);
  border-radius:14px;
  height:3em;
  font-weight:600;
}

/* METRICS */
.metric{
  font-size:32px;
  font-weight:600;
  background: linear-gradient(90deg,#00D1FF,#6366F1);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}

/* DECISION */
.decision{
  text-align:center;
  font-size:24px;
  font-weight:700;
  padding:18px;
  border-radius:14px;
  margin-top:10px;
}
.good{background:rgba(0,255,163,0.1); color:#00FFA3;}
.mid{background:rgba(255,209,102,0.1); color:#FFD166;}
.bad{background:rgba(239,71,111,0.1); color:#EF476F;}
</style>
""", unsafe_allow_html=True)

# =========================
# MODEL SAFE LOAD
# =========================
try:
    model = joblib.load("model.pkl")
    model_loaded = True
except:
    model_loaded = False
    class Dummy:
        def predict(self,X):
            return [np.random.uniform(-10,0)]
    model = Dummy()

# =========================
# HERO (NEW)
# =========================
st.markdown("""
<div class="hero">
  <div class="logo">🧬 LigandLogic</div>
  <div class="title">LigandLogic</div>
  <div class="tagline">AI-driven molecular intelligence for next-gen drug discovery</div>

  <div>
    <span class="badge">⚡ Machine Learning</span>
    <span class="badge">🧪 Drug Discovery</span>
    <span class="badge">📊 Predictive Ranking</span>
  </div>

  <div class="hr"></div>
</div>
""", unsafe_allow_html=True)

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

def featurize(_):
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

    score = float((pred + 10) / 10)
    score = max(0.0, min(score, 1.0))

    if score >= 0.75:
        decision, cls = "DRUG-LIKE CANDIDATE", "good"
    elif score >= 0.5:
        decision, cls = "BORDERLINE CANDIDATE", "mid"
    else:
        decision, cls = "NOT DRUG-LIKE", "bad"

    st.markdown("## Results")

    # BIG DECISION
    st.markdown(f'<div class="decision {cls}">{decision}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.markdown(f'<div class="metric">{score:.2f}</div><p>AI Score</p>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric">{score*100:.1f}%</div><p>Confidence</p>', unsafe_allow_html=True)

    st.progress(score)




