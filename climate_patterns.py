import streamlit as st
import matplotlib.pyplot as plt

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sunshine = [249, 233, 267, 285, 317, 319, 311, 312, 291, 299, 290, 259]
wind = [8, 9, 10, 11, 10, 9, 7, 7, 7, 8, 8, 8]

def show_climate_patterns():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), sharex=True)
    fig.suptitle('Cuba, New Mexico — Monthly Sunshine and Wind Patterns', fontsize=18, fontweight='bold')
    ax1.plot(months, sunshine, color='#E8A035', marker='o', linewidth=2.5, markersize=7)
    ax1.set_title('Monthly Sunshine', fontsize=15)
    ax1.set_ylabel('Sunshine hours per month')
    ax1.grid(True, alpha=0.3)
    ax2.plot(months, wind, color='#2478A5', marker='o', linewidth=2.5, markersize=7)
    ax2.set_title('Monthly Wind Speed', fontsize=15)
    ax2.set_ylabel('Average wind speed (mph)')
    ax2.grid(True, alpha=0.3)
    fig.text(0.5, 0.02, 'Historical monthly climate averages • Preliminary energy assessment', ha='center', fontsize=10)
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    st.pyplot(fig)
    plt.close(fig)

if __name__ == '__main__':
    show_climate_patterns()
