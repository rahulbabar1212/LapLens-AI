import streamlit as st
from pages import dashboard  # you can later add comparison, home

st.set_page_config(page_title="LapLens AI", page_icon="🏁", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, black 0%, #1a1a1a 100%);
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #141414;
    border-right: 1px solid #333;
}
h1, h2, h3, h4 {
    color: #f5f5f5 !important;
    font-family: 'Segoe UI', sans-serif;
}
p {
    color: #cccccc;
    line-height: 1.7;
    font-size: 16px;
    text-align: justify;
}
div.stButton > button:first-child {
    background: linear-gradient(90deg, #ff1e00, #ff7300);
    color: white;
    border-radius: 12px;
    padding: 0.6em 1.4em;
    font-weight: 600;
    border: none;
    transition: 0.3s;
}
div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px rgba(255, 81, 0, 0.6);
}
hr {
    border: none;
    height: 1px;
    background: linear-gradient(to right, #ff1e00, #ff7300);
    margin-top: 2rem;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.info("Developed by **Rahul Babar**  |  © 2025 LapLens AI")

st.title("🏁 LapLens AI")
st.subheader("Your AI-Powered Formula 1 Driver Performance Analyzer")

st.markdown("""
    LapLens AI is an intelligent Formula 1 telemetry analysis platform powered by Machine Learning.  
    It transforms raw racing data into actionable insights — helping engineers and fans visualize 
    each driver’s strengths, weaknesses, and real-time performance patterns.  
    """)

st.button("🚀 Get Started")

st.markdown("<hr>", unsafe_allow_html=True)
st.header("🏎️ Discover the Science of Speed")

st.image("2022-Formula1-Audi-Show-Car-003-2160.jpg", use_container_width=True)
st.markdown("""
    ### Built for Performance
    Formula 1 isn’t just about speed — it’s a science of precision and control.  
    Every car is a masterpiece of engineering, optimized for aerodynamics, traction, 
    and mechanical balance to dominate the racetrack.
    """)

st.image("2022-Formula1-Red-Bull-Racing-RB18-001-2160.jpg", use_container_width=True)
st.markdown("""
    ### Analyze Every Lap
    LapLens AI allows in-depth exploration of telemetry data — from braking force to tire grip.  
    Whether you’re optimizing pit stop strategy or studying cornering efficiency,  
    every detail is visualized in clarity.
    """)

