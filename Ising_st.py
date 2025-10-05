import numpy as np
import random
import streamlit as st
import matplotlib.pyplot as plt 

# Configurazione pagina
st.set_page_config(page_title="2D Ising Model", layout="wide")

# Sidebar solo per parametri fisici
T = st.sidebar.slider("Temperatura (K)", 10, 1000, 50, step=10)
J_input = st.sidebar.slider("Costante di accoppiamento J (cm^-1)", 1, 500, 200) # min. value, max. value, default

# Parametri fissi della simulazione
N = 35         # dimensione griglia fissa
n_steps = 5000 # numero di step fisso
update_every = 5

# Conversione J in Joule
planck_constant = 6.626e-34
c = 3e10
J = J_input * planck_constant * c
k_B = 1.38e-23

# Inizializzazione griglia
Grid = np.random.choice([-1, 1], (N, N))

def compute_neighbors(Grid, i, j):
    up = (i - 1) % N
    down = (i + 1) % N
    left = (j - 1) % N
    right = (j + 1) % N
    return Grid[up, j] + Grid[down, j] + Grid[i, left] + Grid[i, right]

# Placeholder per grafico e magnetizzazione

st.title("Simulazione 2D del Modello di Ising")
st.write("Evoluzione di un reticolo di Spin ferromagneti. Aumentate la temperatura diminuendo la costante di accoppiamento, o viceversa !")


plot_area = st.empty()
magnet_area = st.empty()


# Loop Monte Carlo
for step in range(n_steps):
    i = random.randrange(N)
    j = random.randrange(N)
    selected_spin = Grid[i, j]
    deltaE = 2 * J * selected_spin * compute_neighbors(Grid, i, j)

    if deltaE <= 0 or random.random() < np.exp(-deltaE / (k_B * T)):
        Grid[i, j] *= -1

    # Aggiornamento visualizzazione ogni tot passi
    if step % update_every == 0:
        fig, ax= plt.subplots(figsize =(2,2))
        ax.imshow(Grid, cmap='coolwarm', interpolation='nearest')
        ax.set_title(f"Step {step}/{n_steps}, T = {T} K")
        ax.axis('off')
        plot_area.pyplot(fig)
        plt.close(fig)

        
       
