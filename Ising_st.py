import numpy as np
import random
import matplotlib.pyplot as plt
import streamlit as st
import time

# Configurazione pagina Streamlit
st.set_page_config(page_title="2D Ising Model Simulation", layout="wide")

# Parametri simulazione
T = st.slider("Temperatura (K)", 50, 500, 300, step=10)
N = st.slider("Dimensione reticolo N×N", 10, 100, 20)
n_steps = st.number_input("Numero passi Monte Carlo", 100, 10000, 2000, step=100)
J = 1000 # cm^-1
planck_constant = 6.626 * 10**-34 # J*s
c = 3 * 10**10 # cm/s
J = J * planck_constant * c # Conversione in Joule
k_B = 1.38 * 10**-23 # J/K

# Inizializzazione griglia
Grid = np.random.choice([-1, 1], (N, N))

# Funzione per calcolare la somma dei vicini periodici
def compute_neighbors(Grid, i, j):
    up = (i - 1) % N
    down = (i + 1) % N
    left = (j - 1) % N
    right = (j + 1) % N
    return Grid[up, j] + Grid[down, j] + Grid[i, left] + Grid[i, right]

# Placeholder per grafico dinamico
plot_area = st.empty()

# Loop Monte Carlo
for step in range(int(n_steps)):
    i = random.randrange(N)
    j = random.randrange(N)
    selected_spin = Grid[i, j]

    # Energia di flip
    deltaE = 2 * J * selected_spin * compute_neighbors(Grid, i, j)

    # Regola di Metropolis
    if deltaE <= 0 or random.random() < np.exp(-deltaE / (k_B * T)):
        Grid[i, j] *= -1

    # Aggiornamento visualizzazione ogni tot passi
    if step % (n_steps // 50 + 1) == 0:
        fig, ax = plt.subplots()
        ax.imshow(Grid, cmap='coolwarm', interpolation='nearest')
        ax.set_title(f"Step {step}/{n_steps}, T = {T} K")
        ax.axis('off')
        plot_area.pyplot(fig)
        plt.close(fig)
        time.sleep(0.05)
        
       