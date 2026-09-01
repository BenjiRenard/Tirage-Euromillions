import streamlit as st
import pandas as pd
from config import DRAW_FILE
from src.pipeline import run

st.set_page_config(page_title="EuroMillions Statistical Lab", layout="wide")
st.title("EuroMillions Statistical Lab")
st.caption("Simulation et optimisation statistique — pas un prédicteur de tirage.")

simulations = st.number_input("Simulations Monte Carlo", 10_000, 2_000_000, 100_000, step=10_000)
generations = st.number_input("Générations génétiques", 10, 1_000, 100, step=10)
population = st.number_input("Taille population", 100, 5_000, 500, step=100)
seed = st.number_input("Seed", 0, 1_000_000, 42)

if st.button("Lancer la simulation"):
    with st.spinner("Simulation en cours..."):
        df, results = run(DRAW_FILE, int(simulations), int(generations), int(population), 10, int(seed))

    st.write(f"**{len(df)} tirages analysés**, dernier tirage : {df.iloc[-1]['date'].date()}")

    rows = []
    for rank, (score, ticket) in enumerate(results, 1):
        rows.append({
            "Rang": rank,
            "Numéros": " - ".join(map(str, ticket.numbers)),
            "Étoiles": " - ".join(map(str, ticket.stars)),
            "Score": round(score, 4),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

st.info(
    "Les scores servent uniquement à classer des combinaisons selon les critères "
    "du modèle. Ils ne modifient pas la probabilité mathématique d'un tirage."
)
