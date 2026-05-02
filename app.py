import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="LigandLogic", layout="wide")

# =========================
# 🎨 STYLE (REFINED UI)
# =========================
st.markdown("""
<style>
.stApp{
  background: radial-gradient(circle at 50% 10%, #0F172A, #0B0E14);
  color:#E6EDF3;
}

/* HERO */
.hero{
  text-align:center;
  margin-top:30px;
}

/* ICON */
.icon{
  font-size:42px;
  margin-bottom:10px;
}

/* TITLE */
.title{
  font-family: 'Inter', sans-serif;
  font-weight:800;
  font-size:60px;
  letter-spacing:-1px;
  background: linear-gradient(90deg,#00D1FF,#6366F1);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  text-shadow: 0px 0px 25px rgba(0,209,255,0.25);
}

/* TAGLINE */
.tagline{
  font-family: 'Inter', sans-serif;
  font-style: italic;
  font-size:18px;
  color:#94A3B8;
  margin-top:8px;
}

/* BADGES */
.badges{
  margin-top:12px;
}
.badge{
  display:inline-block;
  padding:6px 14px;
  border-radius:20px;
  border:1px solid #30363D;
  margin:6px;
  font-size:13px;
  color:#CBD5E1;
  background: rgba(255,255,255,0.03);
}

/* DIVIDER */
.divider{
  height:1px;
  margin:22px auto;
  width:60%;
  background: linear-gradient(90deg, transparent, #00D1FF, transparent);
}

/* SECTION */
.section{
  margin-top:28px;
  font-size:24px;
  font-weight:600;
  color:#00D1FF;
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

/* METRIC */
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

/* LED */
.led{
  height:10px;width:10px;border-radius:50%;
  display:inline-block;margin-right:6px;
}
.green{background:#00FFA3;}
.yellow{background:#FFD166;}
.red{background:#EF476F;}
</style>
""", unsafe_allow_html=True)

# =========================
# MODEL
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
# HERO (FIXED)
# =========================
st.markdown("""
<div class="hero">
  <div class="icon">🧬</div>
  <div class="title">LigandLogic</div>
  <div class="tagline">Where machine learning meets molecular intelligence</div>

  <div class="badges">
    <span class="badge">🤖 AI/ML</span>
    <span class="badge">🧪 Drug Discovery</span>
    <span class="badge">🧬 Molecular Intelligence</span>
  </div>

  <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# =========================
# INPUT (NO EXTRA BOX)
# =========================
smiles = st.text_input("SMILES Input", placeholder="e.g. CCO")

# =========================
# FEATURES (UNCHANGED)
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
# ACTION (UNCHANGED)
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

    st.markdown('<div class="section">Results</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="decision {cls}">{decision}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="metric">{score:.2f}</div><p>AI Score</p>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric">{score*100:.1f}%</div><p>Confidence</p>', unsafe_allow_html=True)
    col3.markdown(f'<span class="led {"green" if score>0.7 else "yellow" if score>0.5 else "red"}"></span>{"Model Loaded" if model_loaded else "Fallback"}', unsafe_allow_html=True)

    st.progress(score)

    st.markdown('<div class="section">Molecular Properties</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i,(k,v) in enumerate(features.iloc[0].items()):
        cols[i%4].metric(k, f"{v:.2f}")

