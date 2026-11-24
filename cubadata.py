import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("Cuba 2.5ac vs. JMEC Electricity Data (2019-2025)")

# Timeline
years = np.arange(2019, 2026)

# JMEC Total Electricity Consumption (MWh)
JMEC = np.array([119293.639, 31599.468, 68054.164,
                 73430.865, 32401.281, 32506.292, np.nan])

# Cuba 2.5ac Total Electricity Generation (MWh)
Cuba = np.array([np.nan, np.nan, np.nan, 4963, 6033, 5884, 5764])

# Estimated Total Demand
TotalDemand = JMEC + Cuba

# Create Graph
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(years, JMEC, '-o', linewidth=2, markersize=7, label='JMEC Total MWh')
ax.plot(years, Cuba, '-s', linewidth=2, markersize=7, label='Cuba 2.5ac Total Source')
ax.plot(years, TotalDemand, '-^', linewidth=2, markersize=7, label='Estimated Cuba Demand')

# Graph Formatting
ax.set_title('Cuba 2.5ac Electricity Generation vs. JMEC Demand')
ax.set_xlabel('Year')
ax.set_ylabel('Electricity (MWh)')
ax.legend(loc='best')
ax.set_xticks(years)
ax.set_xlim(2019, 2025)
ax.grid(True)
fig.tight_layout()

st.pyplot(fig)
