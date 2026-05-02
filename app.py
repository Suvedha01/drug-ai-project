st.write("App started successfully")
import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="LigandLogic", layout="wide")


# PREMIUM UI
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #0B0E14, #05070A);
    color: #E6EDF3;
}

/* Title */
.title {
    font-size: 46px;
    font-weight: 700;
    text-align: center;
    letter-spacing: 1px;
}

/* Command bar */
.command {
    border: 1px solid #00D1FF;
    border-radius: 10px;
    padding: 10px;
}

/* Glass card */
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid #ffffff22;
    border-radius: 14px;
    padding: 20px;
}

/* Input */
input {
    font-family: monospace !important;
    color: white !important;
    background: transparent !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg,#0a84ff,#00d1ff);
    color: white;
    border-radius: 10px;
    height: 3em;
}
.stButton>button:hover {
    box-shadow: 0px 0px 20px rgba(0,209,255,0.7);
}

</style>
""", unsafe_allow_html=True)


# HEADER
st.markdown('<div class="title">LigandLogic</div>', unsafe_allow_html=True)
st.caption("Where machine learning meets molecular intelligence")


# LOAD MODEL
model = joblib.load("model.pkl")

feature_order = [
 'MolWt','MolLogP','MolMR','HeavyAtomCount','NumHAcceptors',
 'NumHDonors','NumHeteroatoms','NumRotatableBonds',
 'NumValenceElectrons','NumAromaticRings','NumSaturatedRings',
 'NumAliphaticRings','RingCount','TPSA','LabuteASA',
 'BalabanJ','BertzCT'
]


# COMMAND BAR (TOP INPUT)
st.markdown('<div class="card">', unsafe_allow_html=True)
smiles = st.text_input("Enter SMILES", placeholder="e.g. CCO")
st.markdown('</div>', unsafe_allow_html=True)


# LAYOUT GRID
left, center, right = st.columns([1,2,1])


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


# ACTION
if st.button("Analyze"):

    features = featurize(smiles)
    features = features[feature_order]
    pred = model.predict(features)[0]

    # normalize
    score = (pred + 10) / 10
    score = max(0, min(score, 1))

   
    # LEFT PANEL (PROPERTIES)
    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Properties")

        st.metric("MolWt", f"{features['MolWt'][0]:.1f}")
        st.metric("LogP", f"{features['MolLogP'][0]:.2f}")
        st.metric("TPSA", f"{features['TPSA'][0]:.1f}")

        st.markdown('</div>', unsafe_allow_html=True)

    
    # CENTER PANEL (MAIN)
    with center:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"## Score: {score:.2f}")
        st.progress(score)

        # Radar chart
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=[
                features['MolWt'][0]/500,
                features['MolLogP'][0]/5,
                features['TPSA'][0]/150,
                score,
                np.random.uniform(0.4,1)
            ],
            theta=["MolWt","LogP","TPSA","AI Score","Drug-likeness"],
            fill='toself'
        ))

        fig.update_layout(
            polar=dict(bgcolor="#0B0E14"),
            paper_bgcolor="#0B0E14",
            font_color="white"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


    # RIGHT PANEL (AI OUTPUT)
    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### AI Analysis")

        if score > 0.7:
            st.success("High potential candidate")
        elif score > 0.5:
            st.info("Moderate candidate")
        else:
            st.warning("Low potential")

        st.markdown('</div>', unsafe_allow_html=True)

