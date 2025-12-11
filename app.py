import streamlit as st
import pandas as pd
import plotly.express as px

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Aller à :", 
    ["Introduction", "Exploration", "Graphiques", "Fraudes", "Conclusion"]
)

if page == "Introduction":
    st.title("Analyse des transactions bancaires")
    st.write("Bienvenue dans l'application d'exploration du dataset de fraude.")

elif page == "Exploration":
    st.subheader("Exploration du dataset")
    st.write(df.head())

elif page == "Graphiques":
    st.subheader("Graphiques interactifs")
    st.plotly_chart(fig1)

elif page == "Fraudes":
    st.subheader("Analyse des fraudes")
    st.plotly_chart(fig2)

elif page == "Conclusion":
    st.subheader("Conclusion générale")
    st.write("…")


# Titre de l'application
st.title("Analyse des transactions bancaires - Détection de fraude")

import zipfile
import pandas as pd

# Lire le fichier ZIP dans GitHub
with zipfile.ZipFile("creditcard.zip") as z:
    with z.open("creditcard.csv") as f:
        df = pd.read_csv(f)

st.write(f"Nombre de lignes : {df.shape[0]} - Nombre de colonnes : {df.shape[1]}")

# Histogramme interactif des montants
st.subheader("Histogramme interactif du montant des transactions")
fig_hist = px.histogram(df, x="Amount", nbins=80,
                        labels={"Amount": "Montant (€)"},
                        title="Distribution des montants")
st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("""
**Interprétation :**
### Interprétation

La distribution des montants est extrêmement asymétrique :  
- la majorité des transactions sont de très faible montant,  
- tandis que quelques transactions atteignent des montants très élevés.  

Ce type de distribution est typique des données financières, où un très petit nombre de paiements concentrent une grande partie des montants totaux.  
Ce comportement justifie l’utilisation d’une échelle logarithmique dans certaines visualisations.

À première vue, rien ne permet de différencier directement les transactions frauduleuses des non frauduleuses uniquement via la distribution globale des montants.

""")



# Boxplot selon la classe
st.subheader("Boxplot du montant selon la classe (0 = normal, 1 = fraude)")
fig_box = px.box(df, x="Class", y="Amount", log_y=True,
                 labels={"Class": "Classe", "Amount": "Montant (€)"})
st.plotly_chart(fig_box, use_container_width=True)

st.markdown("""
### Interprétation

Le boxplot montre que les transactions frauduleuses (classe 1) ont des montants plus élevés et plus dispersés que les transactions normales (classe 0).  
Cela suggère que les fraudes impliquent souvent des montants plus importants, même si les médianes restent relativement proches.

La présence de nombreux outliers dans les deux classes montre que les montants varient fortement, mais l'étendue des valeurs est nettement plus marquée pour les fraudes.  
Cela confirme que le montant est une variable pertinente dans la détection de comportements anormaux.

""")


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

st.markdown("""
### Interprétation

### Interprétation

Ce scatter plot représente la relation entre le temps (ordre chronologique des transactions) et les montants.  
On observe :

- une forte concentration de transactions de faible montant à tous les moments de la journée,  
- quelques pics sporadiques de transactions très élevées,  
- mais aucune tendance temporelle évidente permettant de distinguer les fraudes des transactions normales.

Les fraudes apparaissent de manière irrégulière dans le temps et ne semblent pas suivre un schéma particulier.  
Cela indique que la variable *Time* n’est probablement pas un indicateur direct de la fraude, contrairement à d'autres variables dérivées par PCA.

""")
