import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Cuba, NM Energy | ENG220 Team 4",
    page_icon="☀️",
    layout="wide",
)

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(HERE, "ENG220_Cuba Power Data 2019-2025.xlsx")
IMG_PATH = os.path.join(HERE, "cuba_monthly_sunshine_wind.png")


# ---------------------------------------------------------------- data
@st.cache_data
def load_energy_data() -> pd.DataFrame:
    years = np.arange(2019, 2026)
    jmec = np.array([119293.639, 31599.468, 68054.164,
                     73430.865, 32401.281, 32506.292, np.nan])
    cuba = np.array([np.nan, np.nan, np.nan, 4963, 6033, 5884, 5764])
    df = pd.DataFrame({
        "Year": years,
        "JMEC Total MWh": jmec,
        "Cuba 2.5ac Solar MWh": cuba,
    })
    # NaN in either column -> NaN total (same behavior as cubadata.py)
    df["Estimated Cuba Demand MWh"] = df["JMEC Total MWh"] + df["Cuba 2.5ac Solar MWh"]
    return df


@st.cache_data
def load_excel_sheets():
    if not os.path.exists(XLSX_PATH):
        return {}
    try:
        return pd.read_excel(XLSX_PATH, sheet_name=None)
    except Exception:
        return {}


df = load_energy_data()

# ---------------------------------------------------------------- header
st.title("☀️ Energy Use in Cuba, New Mexico")
st.caption("ENG220 Peace Engineering Project · Team 4")

tab_overview, tab_data, tab_climate, tab_dataset, tab_sources = st.tabs(
    ["Overview", "Electricity Data", "Sunshine & Wind", "Raw Dataset", "Sources"]
)

# ---------------------------------------------------------------- overview
with tab_overview:
    st.subheader("Abstract")
    st.write(
        "This project focuses on energy usage in Cuba, New Mexico, primarily its "
        "solar energy usage. Cuba has a relatively small electrical grid, with no "
        "major factories, water filtration centers, or major retailers (the closest "
        "Walmart is in Española). Because of the town's size and limited resources, "
        "expanding the grid has proven difficult. Most homes are powered by solar, "
        "and a small solar farm supplies enough electricity for roughly 1,000 homes."
    )
    st.write(
        "Without a way to increase power to the town, it will be extremely difficult "
        "to build the water filtration plants needed to solve the town's water "
        "crisis. The team is researching how much energy a plant of the needed size "
        "would consume, how to increase Cuba's energy supply, and how Cuba could "
        "model its grid after Taos, which has faced similar issues."
    )

    st.subheader("Team research topics")
    topics = pd.DataFrame(
        [
            ("Matthew", "Taos's energy model"),
            ("Avi", "How much energy the water filtration system uses"),
            ("Kayla", "Expanding Cuba's power grid"),
            ("Channi", "Terrain of Cuba and possible types of energy it can produce"),
            ("Nannette", "Benefits of different energy types and which is best for Cuba"),
        ],
        columns=["Team member", "Topic"],
    )
    st.dataframe(topics, hide_index=True, use_container_width=True)

# ---------------------------------------------------------------- electricity data
with tab_data:
    st.subheader("Cuba 2.5ac Solar Generation vs. JMEC Demand (2019-2025)")

    c1, c2 = st.columns([1, 2])
    with c1:
        year_range = st.slider("Year range", 2019, 2025, (2019, 2025))
    with c2:
        series = st.multiselect(
            "Series to show",
            ["JMEC Total MWh", "Cuba 2.5ac Solar MWh", "Estimated Cuba Demand MWh"],
            default=["JMEC Total MWh", "Cuba 2.5ac Solar MWh", "Estimated Cuba Demand MWh"],
        )

    view = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

    markers = {
        "JMEC Total MWh": "circle",
        "Cuba 2.5ac Solar MWh": "square",
        "Estimated Cuba Demand MWh": "triangle-up",
    }
    fig = go.Figure()
    for col in series:
        fig.add_trace(go.Scatter(
            x=view["Year"], y=view[col], mode="lines+markers", name=col,
            marker=dict(symbol=markers[col], size=9), line=dict(width=3),
            connectgaps=False,
        ))
    fig.update_layout(
        xaxis=dict(title="Year", dtick=1),
        yaxis=dict(title="Electricity (MWh)"),
        legend=dict(orientation="h", y=-0.2),
        height=500,
        margin=dict(l=10, r=10, t=30, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Gaps in a line mean no data for that year (e.g. no solar farm data before "
        "2022 and no JMEC figure for 2025). Estimated demand is only shown where both "
        "values exist."
    )

    # Key metrics
    solar = df["Cuba 2.5ac Solar MWh"].dropna()
    jmec = df["JMEC Total MWh"].dropna()
    m1, m2, m3 = st.columns(3)
    m1.metric("Avg. solar farm output", f"{solar.mean():,.0f} MWh/yr")
    m2.metric("Avg. JMEC consumption", f"{jmec.mean():,.0f} MWh/yr")
    both = df.dropna(subset=["JMEC Total MWh", "Cuba 2.5ac Solar MWh"])
    if not both.empty:
        share = (both["Cuba 2.5ac Solar MWh"] / both["Estimated Cuba Demand MWh"]).mean()
        m3.metric("Solar share of est. demand", f"{share:.1%}",
                  help="Average over years where both datasets exist (2022-2024).")

    st.dataframe(view.set_index("Year").style.format("{:,.0f}", na_rep="n/a"),
                 use_container_width=True)
    st.download_button("Download table as CSV", view.to_csv(index=False),
                       file_name="cuba_energy_2019_2025.csv", mime="text/csv")

# ---------------------------------------------------------------- climate
with tab_climate:
    st.subheader("Monthly sunshine and wind in Cuba, NM")
    if os.path.exists(IMG_PATH):
        st.image(IMG_PATH, use_container_width=True)
    else:
        st.info("Add `cuba_monthly_sunshine_wind.png` to the repo root to show it here.")
    st.caption("Data sources: NSRDB and WRDB data viewers, NOAA U.S. Climate Normals.")

# ---------------------------------------------------------------- raw dataset
with tab_dataset:
    st.subheader("Cuba Power Data 2019-2025 (Excel)")
    sheets = load_excel_sheets()
    if sheets:
        name = st.selectbox("Sheet", list(sheets.keys()))
        st.dataframe(sheets[name], use_container_width=True)
    else:
        st.info(
            "Couldn't load `ENG220_Cuba Power Data 2019-2025.xlsx`. Make sure it's in "
            "the repo root and `openpyxl` is in requirements.txt."
        )

# ---------------------------------------------------------------- sources
with tab_sources:
    st.subheader("Sources")
    st.markdown(
        """
- [Town of Cuba](https://www.cubanm.gov/wp-content/uploads/2025/04/TownofCuba.pdf)
- [Sandoval County CWPP 2012](https://www.emnrd.nm.gov/sfd/wp-content/uploads/sites/4/Sandoval-County-CWPP2012.pdf)
- [La Loma Tank (Cuba) Environmental Assessment, public review](https://www.spa.usace.army.mil/Portals/16/docs/environmental/fonsi/2026/EA_La%20Loma%20Tank%20_Cuba_%20public%20review.pdf?ver=TwKE-rh06vcF-VKf3I3Rmw==&)
- [La Loma Tank (Cuba) Final EA](https://www.spa.usace.army.mil/Portals/16/docs/environmental/fonsi/2026/0167_EA_La%20Loma%20Tank%20-Cuba%20Final%20EA_signed.pdf?ver=fzJXk8Dy77EN7QZjB0fS4A%3D%3D)
- [WRDB data viewer](https://wrdb.nlr.gov/data-viewer)
- [NSRDB data viewer](https://nsrdb.nlr.gov/data-viewer)
- [NOAA U.S. Climate Normals](https://www.ncei.noaa.gov/products/land-based-station/us-climate-normals)
        """
    )
    st.caption("Team reference lists are also in the repo: Kaylas Sources.pdf and Matthew's References.pdf.")
