/* Main Background */
.stApp{

    background:
    radial-gradient(circle at top left, rgba(0,171,228,0.10), transparent 25%),
    radial-gradient(circle at bottom right, rgba(197,173,197,0.18), transparent 30%),
    linear-gradient(
        135deg,
        #E9F1FA 0%,
        #F8FBFF 45%,
        #FFFFFF 100%
    );

    font-family:'Inter', sans-serif;

    color:#1E293B;
}

/* Floating Glow */
.stApp::before{
    content:'';

    position:fixed;

    width:420px;
    height:420px;

    background:rgba(0,171,228,0.12);

    border-radius:50%;

    filter:blur(120px);

    top:-100px;
    left:-100px;

    animation:float1 10s ease-in-out infinite alternate;

    z-index:-1;
}

.stApp::after{
    content:'';

    position:fixed;

    width:420px;
    height:420px;

    background:rgba(197,173,197,0.20);

    border-radius:50%;

    filter:blur(120px);

    bottom:-100px;
    right:-100px;

    animation:float2 12s ease-in-out infinite alternate;

    z-index:-1;
}

/* Premium Title */
.title{

    font-family:'Orbitron', sans-serif;

    font-size:68px;

    font-weight:800;

    letter-spacing:-2px;

    background:linear-gradient(
        90deg,
        #00ABE4,
        #4A90E2,
        #C5ADC5
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;

    text-shadow:
    0 0 10px rgba(0,171,228,0.18);
}

/* Tagline */
.tagline{

    margin-top:10px;

    font-size:17px;

    color:#5B6B82;

    font-style:italic;

    letter-spacing:0.5px;
}

/* Glass Card */
.glass{

    margin-top:30px;

    background:rgba(255,255,255,0.75);

    backdrop-filter:blur(20px);

    border:1px solid rgba(255,255,255,0.55);

    border-radius:26px;

    padding:30px;

    box-shadow:
    0 8px 30px rgba(0,0,0,0.08);
}

/* Input */
input{

    background:rgba(255,255,255,0.95)!important;

    color:#111827!important;

    border-radius:14px!important;

    border:1px solid rgba(0,171,228,0.18)!important;

    font-family:monospace!important;
}

/* Analyze Button */
.stButton>button{

    width:100%;

    background:linear-gradient(
        90deg,
        #00ABE4,
        #4A90E2,
        #B2B5E0
    );

    border:none;

    border-radius:16px;

    color:white;

    font-size:16px;

    font-weight:700;

    padding:14px;

    transition:0.3s ease;

    box-shadow:
    0 4px 15px rgba(0,171,228,0.22);
}

.stButton>button:hover{

    transform:scale(1.02);

    box-shadow:
    0 8px 25px rgba(0,171,228,0.30);
}

/* Result Colors */

.good{
    background:rgba(0,171,228,0.10);
    color:#0077B6;
    border:1px solid rgba(0,171,228,0.22);
}

.mid{
    background:rgba(197,173,197,0.18);
    color:#7C6280;
    border:1px solid rgba(197,173,197,0.28);
}

.bad{
    background:rgba(255,107,107,0.10);
    color:#D62828;
    border:1px solid rgba(255,107,107,0.22);
}
