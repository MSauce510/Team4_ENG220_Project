import numpy as np
import matplotlib.pyplot as plt

# Cuba 2.5ac vs. JMEC Electricity Data (2019-2025)

# Timeline
years = np.arange(2019, 2026)

# JMEC Total Electricity Consumption (MWh)
JMEC = [119293.639, 31599.468, 68054.164,
        73430.865, 32401.281, 32506.292, np.nan]

# Cuba 2.5ac Total Electricity Generation (MWh)
Cuba = [np.nan, np.nan, np.nan, 4963, 6033, 5884, 5764]

# Estimated Total Demand
TotalDemand = np.array(JMEC) + np.array(Cuba)

# Create Graph
plt.figure(figsize=(10, 6))

plt.plot(years, JMEC, '-o', linewidth=2,
         markersize=7, label='JMEC Total MWh')

plt.plot(years, Cuba, '-s', linewidth=2,
         markersize=7, label='Cuba 2.5ac Total Source')

plt.plot(years, TotalDemand, '-^', linewidth=2,
         markersize=7, label='Estimated Cuba Demand')

# Graph Formatting
plt.title('Cuba 2.5ac Electricity Generation vs. JMEC Demand')
plt.xlabel('Year')
plt.ylabel('Electricity (MWh)')

plt.legend(loc='best')

plt.xticks(years)
plt.xlim(2019, 2025)

plt.grid(True)
plt.tight_layout()
plt.show()