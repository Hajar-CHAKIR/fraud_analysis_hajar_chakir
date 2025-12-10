import streamlit as st
import pandas as pd
import plotly.express as px

# Titre de l'application
st.title("Analyse des transactions bancaires - Détection de fraude")

# Chargement du dataset
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/creditcard.csv")

st.write(f"Nombre de lignes : {df.shape[0]} - Nombre de colonnes : {df.shape[1]}")

# Histogramme interactif des montants
st.subheader("Histogramme interactif du montant des transactions")
fig_hist = px.histogram(df, x="Amount", nbins=80,
                        labels={"Amount": "Montant (€)"},
                        title="Distribution des montants")
st.plotly_chart(fig_hist, use_container_width=True)

# Boxplot selon la classe
st.subheader("Boxplot du montant selon la classe (0 = normal, 1 = fraude)")
fig_box = px.box(df, x="Class", y="Amount", log_y=True,
                 labels={"Class": "Classe", "Amount": "Montant (€)"})
st.plotly_chart(fig_box, use_container_width=True)

# Scatter Time vs Amount coloré par Class
st.subheader("Relation temps / montant (échantillon)")
sample_df = df.sample(5000, random_state=42)
fig_scatter = px.scatter(
    sample_df,
    x="Time",
    y="Amount",
    color="Class",
    log_y=True,
    labels={"Time": "Temps (sec)", "Amount": "Montant (€)", "Class": "Classe"},
    title="Time vs Amount (échantillon)"
)
st.plotly_chart(fig_scatter, use_container_width=True)
