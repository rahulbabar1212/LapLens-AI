import streamlit as st
import fastf1
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import plotly.express as px
import os

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="LapLens AI - Lap Time Predictor", page_icon="🏎️", layout="wide")

# ========== CUSTOM STYLES ==========
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, black 0%, #1a1a1a 100%);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #141414;
    border-right: 1px solid #333;
}
h1, h2, h3 {
    color: #ff7300 !important;
}
p, label, div {
    color: #cccccc !important;
}
div.stButton > button:first-child {
    background: linear-gradient(90deg, #ff1e00, #ff7300);
    color: white;
    border-radius: 10px;
    padding: 0.6em 1.2em;
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

# ========== FASTF1 CACHE ==========
if not os.path.exists('cache'):
    os.makedirs('cache')
fastf1.Cache.enable_cache('cache')

# ========== HEADER ==========
st.title("🏁 LapLens AI - Lap Time Predictor")
st.markdown(
    "<p style='color:#bbbbbb;'>AI-driven Lap Time Prediction using Formula 1 telemetry data</p>",
    unsafe_allow_html=True
)

# ========== SIDEBAR ==========
st.sidebar.header("⚙️ Input Race Details")
year = st.sidebar.selectbox("Select Year", list(range(2015, 2025))[::-1])
gp = st.sidebar.text_input("Enter Grand Prix (e.g., Bahrain, Monaco)", "Bahrain")
session_type = st.sidebar.selectbox("Select Session", ["Practice 1", "Qualifying", "Race"])
driver = st.sidebar.text_input("Enter Driver Code (e.g., VER, HAM, LEC)", "VER")

# ========== FETCH DATA ==========
if st.sidebar.button("🚀 Train Lap Predictor"):
    try:
        with st.spinner("Loading race session and training model..."):
            session = fastf1.get_session(year, gp, session_type)
            session.load()

            laps = session.laps.pick_driver(driver)
            if laps.empty:
                st.warning(f"No lap data found for driver {driver}.")
            else:
                laps = laps.reset_index(drop=True)

                # Extract lap data
                lap_data = laps[['LapNumber', 'LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time',
                                 'SpeedI1', 'SpeedI2', 'SpeedFL', 'Compound']].dropna()

                # Convert timedelta to seconds
                lap_data['LapTime'] = lap_data['LapTime'].dt.total_seconds()
                lap_data['Sector1Time'] = lap_data['Sector1Time'].dt.total_seconds()
                lap_data['Sector2Time'] = lap_data['Sector2Time'].dt.total_seconds()
                lap_data['Sector3Time'] = lap_data['Sector3Time'].dt.total_seconds()

                # Encode compound type
                lap_data['Compound'] = lap_data['Compound'].astype('category').cat.codes

                # Split features and target
                X = lap_data.drop(columns=['LapTime'])
                y = lap_data['LapTime']

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                model = RandomForestRegressor(n_estimators=200, random_state=42)
                model.fit(X_train, y_train)

                # Predictions
                y_pred = model.predict(X_test)
                mae = mean_absolute_error(y_test, y_pred)

                st.success(f"✅ Model trained successfully! MAE: {mae:.3f} seconds")

                # Plot comparison
                fig = px.scatter(
                    x=y_test,
                    y=y_pred,
                    labels={"x": "Actual Lap Time (s)", "y": "Predicted Lap Time (s)"},
                    title="Actual vs Predicted Lap Times"
                )
                fig.update_traces(marker=dict(color="#ff7300", size=10, opacity=0.8))
                fig.update_layout(
                    plot_bgcolor="black",
                    paper_bgcolor="black",
                    font=dict(color="white"),
                    height=600
                )
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("<hr>", unsafe_allow_html=True)
                st.header("🎯 Predict a Custom Lap Time")

                col1, col2, col3 = st.columns(3)
                with col1:
                    s1 = st.number_input("Sector 1 Time (s)", min_value=20.0, max_value=50.0, value=30.0)
                    s2 = st.number_input("Sector 2 Time (s)", min_value=20.0, max_value=50.0, value=35.0)
                with col2:
                    s3 = st.number_input("Sector 3 Time (s)", min_value=20.0, max_value=50.0, value=32.0)
                    compound = st.selectbox("Tyre Compound", ["Soft", "Medium", "Hard"])
                with col3:
                    sp1 = st.number_input("Speed I1 (km/h)", min_value=200, max_value=350, value=290)
                    sp2 = st.number_input("Speed I2 (km/h)", min_value=200, max_value=350, value=300)
                    spfl = st.number_input("Speed FL (km/h)", min_value=200, max_value=350, value=310)

                compound_code = {"Soft": 0, "Medium": 1, "Hard": 2}[compound]
                input_data = pd.DataFrame([[1, s1, s2, s3, sp1, sp2, spfl, compound_code]],
                                          columns=X.columns)

                predicted_time = model.predict(input_data)[0]
                st.markdown(f"### 🏎️ Predicted Lap Time: **{predicted_time:.3f} seconds**")

                st.caption("Model uses telemetry and sector data to predict overall lap time.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
