import streamlit as st
import requests
import pandas as pd

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="BioBound",
    page_icon="🧬",
    layout="centered"
)

# =========================================
# FUTURISTIC TECH-BIO UI
# =========================================
st.markdown("""
<style>

/* ---------------- BACKGROUND ---------------- */

.stApp{
    background:
    radial-gradient(circle at top left, rgba(0,255,255,0.12), transparent 25%),
    radial-gradient(circle at bottom right, rgba(255,0,128,0.10), transparent 25%),
    linear-gradient(135deg,#050816,#091120,#050816);

    color:#EAF2FF;
    overflow:hidden;
}

/* Floating animated glow */
.stApp::before{
    content:'';
    position:fixed;
    width:500px;
    height:500px;
    background:rgba(0,212,255,0.10);
    border-radius:50%;
    filter:blur(120px);
    top:-100px;
    left:-100px;
    animation:floatGlow 10s ease-in-out infinite alternate;
    z-index:-1;
}

.stApp::after{
    content:'';
    position:fixed;
    width:450px;
    height:450px;
    background:rgba(183,0,255,0.12);
    border-radius:50%;
    filter:blur(120px);
    bottom:-100px;
    right:-100px;
    animation:floatGlow2 12s ease-in-out infinite alternate;
    z-index:-1;
}

/* Glow animations */
@keyframes floatGlow{
    from{
        transform:translateY(0px) translateX(0px);
    }
    to{
        transform:translateY(60px) translateX(40px);
    }
}

@keyframes floatGlow2{
    from{
        transform:translateY(0px) translateX(0px);
    }
    to{
        transform:translateY(-60px) translateX(-40px);
    }
}

/* ---------------- HEADER ---------------- */

.hero{
    text-align:center;
    margin-top:30px;
    animation:fadeIn 1.5s ease;
}

/* Floating DNA */
.dna{
    font-size:70px;
    margin-bottom:10px;
    animation:floating 4s ease-in-out infinite;
    filter:drop-shadow(0 0 18px rgba(0,212,255,0.5));
}

/* Title */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;800&display=swap');

.title{

    font-family:'Orbitron', sans-serif;

    font-size:68px;

    font-weight:800;

    letter-spacing:-1px;

    margin-top:-5px;

    background:linear-gradient(
    90deg,
    #ffffff 0%,
    #7DF9FF 35%,
    #C084FC 70%,
    #ffffff 100%
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;

    text-shadow:
    0 0 12px rgba(125,249,255,0.35),
    0 0 28px rgba(192,132,252,0.25);

    animation:titleGlow 4s ease-in-out infinite alternate;
}

@keyframes titleGlow{

    from{
        filter:drop-shadow(0 0 8px rgba(125,249,255,0.25));
    }

    to{
        filter:drop-shadow(0 0 18px rgba(192,132,252,0.45));
    }
}

/* Tagline */
.tagline{
    margin-top:10px;

    font-size:18px;
    font-style:italic;

    color:#B8C7E0;
    letter-spacing:0.5px;
}

/* Floating */
@keyframes floating{
    0%{
        transform:translateY(0px);
    }
    50%{
        transform:translateY(-10px);
    }
    100%{
        transform:translateY(0px);
    }
}

/* Fade in */
@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(20px);
    }
    to{
        opacity:1;
        transform:translateY(0px);
    }
}

/* ---------------- INPUT ---------------- */

input{
    background:rgba(255,255,255,0.05)!important;

    color:white!important;

    border-radius:16px!important;

    border:1px solid rgba(125,249,255,0.25)!important;

    font-family:monospace!important;

    padding:12px!important;
}

/* ---------------- BUTTON ---------------- */

.stButton>button{

    width:100%;

    background:linear-gradient(
    90deg,
    #00D4FF,
    #7B61FF,
    #D946EF
    );

    border:none;

    color:white;

    font-size:16px;
    font-weight:700;

    border-radius:16px;

    padding:14px;

    transition:0.3s ease;

    box-shadow:0 0 20px rgba(0,212,255,0.35);
}

/* Hover effect */
.stButton>button:hover{
    transform:scale(1.03);

    box-shadow:
    0 0 30px rgba(0,212,255,0.55),
    0 0 50px rgba(217,70,239,0.35);
}

/* ---------------- RESULT ---------------- */

.result{

    margin-top:25px;

    text-align:center;

    font-size:30px;
    font-weight:800;

    padding:18px;

    border-radius:18px;

    animation:fadeIn 1s ease;
}

.good{
    background:rgba(0,255,163,0.12);
    color:#00FFA3;
    border:1px solid rgba(0,255,163,0.25);
}

.mid{
    background:rgba(255,209,102,0.12);
    color:#FFD166;
    border:1px solid rgba(255,209,102,0.25);
}

.bad{
    background:rgba(255,107,107,0.12);
    color:#FF6B6B;
    border:1px solid rgba(255,107,107,0.25);
}

/* ---------------- METRIC CARDS ---------------- */

.metric-card{

    background:rgba(255,255,255,0.05);

    border:1px solid rgba(255,255,255,0.08);

    border-radius:20px;

    padding:20px;

    text-align:center;

    margin-top:14px;

    transition:0.3s ease;
}

.metric-card:hover{
    transform:translateY(-4px) scale(1.02);

    border:1px solid rgba(125,249,255,0.25);

    box-shadow:0 0 20px rgba(0,212,255,0.15);
}

.metric-title{
    color:#B8C7E0;
    font-size:14px;
}

.metric-value{
    font-size:30px;
    font-weight:700;

    margin-top:6px;

    background:linear-gradient(
    90deg,
    #7DF9FF,
    #D946EF
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

/* Divider */
.divider{
    margin:28px 0;

    height:1px;

    background:linear-gradient(
    90deg,
    transparent,
    rgba(125,249,255,0.35),
    transparent
    );
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================
st.markdown("""
<div class="hero">

<div class="dna">🧬</div>

<div class="title">
BioBound
</div>

<div class="tagline">
Where Molecular Intelligence Begins
</div>

</div>
""", unsafe_allow_html=True)

# =========================================
# MAIN CARD
# =========================================
st.markdown('<div class="glass">', unsafe_allow_html=True)

smiles = st.text_input(
    "Enter SMILES",
    placeholder="e.g. CC(=O)OC1=CC=CC=C1C(=O)O"
)

# =========================================
# PUBCHEM API
# =========================================
def get_properties(smiles):

    try:

        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,TPSA/JSON"

        response = requests.get(url, timeout=10)

        data = response.json()

        props = data["PropertyTable"]["Properties"][0]

        return {
            "Molecular Weight": float(props.get("MolecularWeight", 0) or 0),
            "LogP": float(props.get("XLogP", 0) or 0),
            "H Donors": float(props.get("HBondDonorCount", 0) or 0),
            "H Acceptors": float(props.get("HBondAcceptorCount", 0) or 0),
            "TPSA": float(props.get("TPSA", 0) or 0)
        }

    except:
        return None

# =========================================
# ANALYSIS
# =========================================
if st.button("Analyze Molecule"):

    if not smiles:
        st.error("Please enter a SMILES string")
        st.stop()

    props = get_properties(smiles)

    if props is None:
        st.error("Invalid SMILES or API Error")
        st.stop()

    # =========================================
    # QED-LIKE SCORING
    # =========================================
    score = 1.0

    score -= abs(props["Molecular Weight"] - 350) / 1000
    score -= abs(props["LogP"] - 2.5) / 10
    score -= abs(props["TPSA"] - 75) / 300

    if props["H Donors"] > 6:
        score -= 0.1

    if props["H Acceptors"] > 12:
        score -= 0.1

    score = max(0.0, min(score, 1.0))

    # =========================================
    # CLASSIFICATION
    # =========================================
    if score >= 0.60:
        decision = "DRUG-LIKE"
        cls = "good"

    elif score >= 0.35:
        decision = "MODERATE"
        cls = "mid"

    else:
        decision = "NOT DRUG-LIKE"
        cls = "bad"

    # =========================================
    # RESULT
    # =========================================
    st.markdown(
        f'<div class="result {cls}">{decision}</div>',
        unsafe_allow_html=True
    )

    st.progress(score)

    # =========================================
    # METRICS
    # =========================================
    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                Drug-Likeness Score
                </div>

                <div class="metric-value">
                {score:.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                Confidence
                </div>

                <div class="metric-value">
                {score*100:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )

    st.subheader("Molecular Properties")

    df = pd.DataFrame([props])

    st.dataframe(df, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


