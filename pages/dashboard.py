import streamlit as st
import fastf1
import pandas as pd
import plotly.graph_objects as go
import os

# =========================
# Cache Setup
# =========================
if not os.path.exists('cache'):
    os.makedirs('cache')
fastf1.Cache.enable_cache('cache')

# =========================
# Page Configuration
# =========================
st.set_page_config(page_title="LapLens AI Dashboard", page_icon="🏁", layout="wide")

# =========================
# Custom F1-Themed CSS
# =========================
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
    color: #f5f5f5 !important;
}
p, div, label {
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
[data-testid="stHeader"] {
    background: none;
}
.stDataFrame {
    border: 1px solid #333 !important;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================
st.title("🏁 LapLens AI - Formula 1 Dashboard")
st.subheader("Analyze Telemetry, Race Results, and Driver Performance")

st.sidebar.info("Developed by **Rahul Babar**  |  © 2025 LapLens AI")

# =========================
# Sidebar Inputs
# =========================
st.sidebar.header("⚙️ Race Details")
year = st.sidebar.selectbox("Select Year", list(range(2015, 2025))[::-1])
gp = st.sidebar.text_input("Enter Grand Prix (e.g., Bahrain, Monaco)", "Bahrain")
session_type = st.sidebar.selectbox("Select Session", ["Practice 1", "Qualifying", "Race"])
driver = st.sidebar.text_input("Enter Driver Code (e.g., VER, HAM, LEC)", "VER")

# =========================
# Fetch Data
# =========================
if st.sidebar.button("🚀 Fetch Race Data"):
    try:
        with st.spinner("Fetching and processing race data..."):
            session = fastf1.get_session(year, gp, session_type)
            session.load()

        st.success(f"✅ Loaded {gp} {session_type} session ({year}) successfully!")

        # =============== Race Summary ===============
        st.markdown("## 📋 Race Summary")
        info = {
            "Year": year,
            "Grand Prix": gp,
            "Session Type": session_type,
            "Track": session.event['Location'],
            "Country": session.event['Country'],
            "Date": session.date.strftime('%Y-%m-%d'),
            "Total Laps": len(session.laps)
        }
        st.table(pd.DataFrame(info.items(), columns=["Parameter", "Value"]))

        # =============== Weather Data ===============
        st.markdown("## 🌡️ Weather Data")
        if not session.weather_data.empty:
            st.dataframe(session.weather_data.head(5))
        else:
            st.warning("No weather data available.")

        # =============== Race Results ===============
        st.markdown("## 🏁 Top 10 Results")
        results = session.results[['Abbreviation', 'Position', 'Time', 'Points', 'TeamName']]
        st.dataframe(results.head(10))

        # =============== Driver Lap Data ===============
        laps = session.laps.pick_driver(driver)
        if laps.empty:
            st.warning(f"No lap data found for driver {driver}.")
        else:
            st.markdown(f"## 📊 {driver} Lap Summary")
            lap_summary = laps[['LapNumber', 'LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time', 'Compound', 'TrackStatus']]
            st.dataframe(lap_summary.head(10))

            fastest = laps.pick_fastest()
            tel = fastest.get_telemetry()

            # =============== Telemetry Visualizations ===============
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("## 📈 Telemetry Visualization (3D)")

            show_speed = st.checkbox("Show Speed vs Distance vs Throttle", True)
            show_rpm = st.checkbox("Show RPM vs Distance vs Gear", True)
            show_brake = st.checkbox("Show Brake vs DRS vs Distance", True)

            def plot_3d(x, y, z, color, title, xlbl, ylbl, zlbl):
                fig = go.Figure(data=[go.Scatter3d(
                    x=x, y=y, z=z,
                    mode='markers',
                    marker=dict(size=4, color=color, colorscale='Inferno', opacity=0.9),
                )])
                fig.update_layout(
                    title=f"<b>{title}</b>",
                    scene=dict(
                        xaxis_title=xlbl,
                        yaxis_title=ylbl,
                        zaxis_title=zlbl,
                        bgcolor='black'
                    ),
                    paper_bgcolor='black',
                    font=dict(color="white"),
                    margin=dict(l=0, r=0, b=0, t=50),
                    height=600
                )
                st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                if show_speed:
                    plot_3d(tel['Distance'], tel['Speed'], tel['Throttle'],
                            tel['Speed'], "Speed vs Distance vs Throttle", "Distance (m)", "Speed (km/h)", "Throttle (%)")
            with col2:
                if show_rpm:
                    plot_3d(tel['Distance'], tel['RPM'], tel['nGear'],
                            tel['RPM'], "RPM vs Distance vs Gear", "Distance (m)", "RPM", "Gear")

            if show_brake:
                plot_3d(tel['Distance'], tel['Brake'], tel['DRS'],
                        tel['Brake'], "Brake vs DRS vs Distance", "Distance (m)", "Brake", "DRS")

            # =============== Tyre Compound Usage ===============
            st.markdown("## 🛞 Tyre Compound Usage")
            compound_counts = laps['Compound'].value_counts().reset_index()
            compound_counts.columns = ['Tyre Compound', 'Usage Count']
            st.bar_chart(compound_counts.set_index('Tyre Compound'))
            st.caption("Displays which tyre compounds were most used during the session.")

        st.success("✅ Race data visualization complete!")

    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
