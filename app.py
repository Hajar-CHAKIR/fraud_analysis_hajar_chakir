import streamlit as st 
import pandas as pd
import plotly.express as px
import zipfile

# -----------------------------
# Chargement du dataset
# -----------------------------
with zipfile.ZipFile("creditcard.zip") as z:
    with z.open("creditcard.csv") as f:
        df = pd.read_csv(f)

# Échantillon pour les graphes lourds
sample_df = df.sample(5000, random_state=42)

# -----------------------------
# Sidebar (navigation facultative)
# -----------------------------
st.sidebar.title("Navigation")
st.sidebar.markdown("""
Ce menu vous permet d'aller directement à une section :
- Introduction  
- Exploration  
- Graphiques  
- Fraudes  
- Conclusion  
""")

# -----------------------------
# Introduction
# -----------------------------
st.title("Analyse des transactions bancaires - Détection de fraude")
st.markdown("""
Cette application explore un dataset réel de transactions bancaires comprenant des opérations frauduleuses.  
Elle permet d'analyser les distributions, les corrélations et les comportements typiques des fraudes.
""")

st.write(f"**Nombre de lignes :** {df.shape[0]}")
st.write(f"**Nombre de colonnes :** {df.shape[1]}")

st.markdown("---")

# -----------------------------
# Exploration
# -----------------------------
st.header("Exploration du dataset")

st.subheader("Aperçu des premières lignes")
st.write(df.head())

st.subheader("Statistiques descriptives")
st.write(df.describe())

st.markdown("---")

# -----------------------------
# Graphiques
# -----------------------------
st.header("Visualisations interactives")

# Histogramme
st.subheader("Histogramme interactif du montant des transactions")
fig_hist = px.histogram(df, x="Amount", nbins=80,
                        labels={"Amount": "Montant (€)"},
                        title="Distribution des montants")
st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("""
### Interprétation  
La distribution des montants est extrêmement asymétrique :
- majorité de petites transactions  
- quelques transactions très élevées  

Ce comportement est typique des données financières et justifie l'usage d'échelles logarithmiques.
""")

# Boxplot
st.subheader("Boxplot du montant selon la classe")
fig_box = px.box(df, x="Class", y="Amount", log_y=True,
                 labels={"Class": "Classe", "Amount": "Montant (€)"})
st.plotly_chart(fig_box, use_container_width=True)

st.markdown("""
### Interprétation  
Les transactions frauduleuses impliquent souvent des montants plus élevés
et plus dispersés que les transactions normales.
""")

# Scatter
st.subheader("Relation temps / montant (échantillon)")
fig_scatter = px.scatter(
    sample_df,
    x="Time",
    y="Amount",
    color="Class",
    color_discrete_map={
        0: "#4a4a4a",   # gris foncé
        1: "#d62728"    # rouge pour bien distinguer la fraude
    },
    log_y=True,
    labels={"Time": "Temps (sec)", "Amount": "Montant (€)", "Class": "Classe"},
    title="Time vs Amount (échantillon)"
)
st.plotly_chart(fig_scatter, use_container_width=True)


st.markdown("""
### Interprétation  
Les fraudes apparaissent aléatoirement dans le temps.  
La variable *Time* semble donc peu informative pour la prédiction directe.
""")

st.markdown("---")

# -----------------------------
# Fraudes
# -----------------------------
st.header("Analyse des transactions frauduleuses")

fraud = df[df["Class"] == 1]
nonfraud = df[df["Class"] == 0]

st.write(f"**Nombre de fraudes :** {len(fraud)}")
st.write(f"**Nombre de transactions normales :** {len(nonfraud)}")

st.subheader("Comparaison des montants (fraudes vs non-fraudes)")
fig_fraud = px.box(df, x="Class", y="Amount", log_y=True,
                   labels={"Class": "Classe", "Amount": "Montant (€)"})
st.plotly_chart(fig_fraud, use_container_width=True, key="fraud_boxplot")

st.markdown("""
### Analyse  
Les transactions frauduleuses montrent davantage d'outliers 
et une variabilité plus forte, ce qui en fait un indicateur utile
pour détecter des anomalies.
""")


st.markdown("---")

# -----------------------------
# Conclusion
# -----------------------------
st.header("Conclusion")

st.markdown("""
### Résumé de l'analyse

- Le dataset est **fortement déséquilibré** : seulement 0.17% de fraudes.  
- Les montants des transactions frauduleuses sont souvent plus élevés.  
- Certaines variables PCA montrent une corrélation forte avec la fraude (ex : V14, V17).  
- La variable *Time* est peu discriminante.  
- Les fraudes apparaissent sans motif temporel clair.  

Cette analyse constitue une base pour un futur modèle de machine learning visant à détecter les transactions frauduleuses.
""")

st.success("Merci d'avoir exploré cette application !")
