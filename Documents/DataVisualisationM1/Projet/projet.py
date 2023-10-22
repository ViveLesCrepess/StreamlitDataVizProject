import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image
import altair as alt

st.set_page_config(page_title="Analyse d'accidents routiers",
                   page_icon="🚗", layout="wide")


# Les valeurs à supprimer : pr / pr1 / lartpc / V1 / V2 / voie car ne répondent pas à la question
df = pd.read_csv("lieux-2022.csv", delimiter=';')
df["larrout"] = pd.to_numeric(
    df["larrout"].str.replace(',', '.'), errors='coerce')

df = df.drop("larrout", axis=1)
df = df.drop("v2", axis=1)
df = df.drop("v1", axis=1)
df = df.drop("voie", axis=1)
df = df.drop("pr", axis=1)
df = df.drop("pr1", axis=1)
df = df.drop("lartpc", axis=1)

# Les données qu'on va utiliser comporte beaucoup de -1 "non renseigné", on va crée un nouvel dataframe en gardant que les données pertinentes
df_sans_les_non_renseigner = df[(
    df["circ"] != -1) & (df["plan"] != -1) & (df["infra"] != -1) & (df["surf"] != -1) & (df["situ"] != -1) & (df["prof"] != -1) & (df["circ"] != -1)]

st.title("Projet en data visualisation : Le type de route a-t-il un impact sur le nombre et le type d’accident ?")

# Chargement de l'image streamlit
image1 = Image.open('important.jpg')
st.image(image1, caption="Prévention")
st.title("Attention ... la route peut vous conduire à une morte certaine 😱")


image2 = Image.open('accident.jpg')
st.image(image2, caption="Accident de voiture")

# Menu streamlit
st.sidebar.header('Menu de Navigation')

st.sidebar.markdown(
    '[Aller à Section 1 : Type de route avec le plus de d\'accident](#section-1)')
st.sidebar.markdown(
    '[Aller à Section 2 : La catégorie de route en fonction du régime de circulation](#section-2)')
st.sidebar.markdown(
    '[Aller à Section 3 : La catégorie de route en fonction du tracé en plan](#section-3)')
st.sidebar.markdown(
    '[Aller à Section 4 : L\'infrastructure en fonction du régime de circulation](#section-4)')
st.sidebar.markdown(
    '[Aller à Section 5 : Le tracé en plan en fonction du profil de déclivité de la route](#section-5)')
st.sidebar.markdown(
    '[Aller à Section 6 : La situation de l\'accident en fonction de l\'état de la surface](#section-6)')
st.sidebar.markdown(
    '[Aller à Section 7 : La situation de l\'accident en fonction de la catégorie de route](#section-7)')
st.sidebar.markdown(
    '[Aller à Section 8 : La catégorie de route en fonction de la vitesse maximale](#section-8)')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Compréhension de la colonne catr
st.write('## Section 1')
st.subheader("Type de route avec le plus d'accident :")

catr = df_sans_les_non_renseigner["catr"]
label = ["Autoroute", "Route nationale", "Route Départementale", "Voie Communale", "Hors réseau public",
         "Parc de stationnement ouvert à la circulation publique", "Routes de métropole urbaine", "Autre"]
fig1 = px.pie(values=catr.value_counts(), names=label, color_discrete_map={"Autoroute": "#3498db", "Route nationale": "#2979b8", "Route Départementale": "#1c6ea4",
                                                                           "Voie Communale": "#185a8d", "Hors réseau public": "#154f77", "Parc de stationnement ouvert à la circulation publique": "#133e60", "Routes de métropole urbaine": "#112d49", "Autre": "#0e2334"})
st.plotly_chart(fig1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# lien entre catr et circ
st.write('## Section 2')
st.subheader("La catégorie de route en fonction du régime de circulation")

catr_labels = {
    1: '1 – Autoroute',
    2: '2 – Route nationale',
    3: '3 – Route Départementale',
    4: '4 – Voie Communales',
    5: '5 – Hors réseau public',
    6: '6 – Parc de stationnement ouvert à la circulation publique',
    7: '7 – Routes de métropole urbaine',
    9: '9 – autre'
}

df_sans_les_non_renseigner['catr'] = df_sans_les_non_renseigner['catr'].map(
    catr_labels)

faire_la_liaison = df_sans_les_non_renseigner.groupby(
    ['catr', 'circ']).size().unstack().reset_index()
faire_la_liaison_melted = pd.melt(
    faire_la_liaison, id_vars='catr', var_name='circ', value_name='Nombre de Trajets')
fig2 = px.bar(faire_la_liaison_melted, x='catr',
              y='Nombre de Trajets', color='circ')

legend_labels = {
    '1': '1 : A sens unique',
    '2': '2 : Bidirectionnelle',
    '3': '3 : A chaussées séparées',
    '4': '4 : Avec voies d’affectation variable'
}

fig2.update_traces(marker_line_width=1)
fig2.for_each_trace(lambda t: t.update(name=legend_labels.get(t.name, t.name)))

st.plotly_chart(fig2, use_container_width=True)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# catr et plan
st.write('## Section 3')
st.subheader("La catégorie de route en fonction du tracé en plan")

faire_la_liaison = df_sans_les_non_renseigner.groupby(
    ['catr', 'plan']).size().unstack().reset_index()
faire_la_liaison_melted = pd.melt(
    faire_la_liaison, id_vars='catr', var_name='plan', value_name='Nombre de Trajets')
fig1 = px.line(faire_la_liaison_melted, x='catr',
               y='Nombre de Trajets', color='plan')

legend_labels = {
    '1': '1 : Partie rectiligne',
    '2': '2 : En courbe à gauche',
    '3': '3 : En courbe à droites',
    '4': '4 : En « S »'
}

fig1 = px.line(faire_la_liaison_melted, x='catr',
               y='Nombre de Trajets', color='plan')
fig1.update_traces(marker_line_width=1)
fig1.for_each_trace(lambda t: t.update(name=legend_labels.get(t.name, t.name)))

st.plotly_chart(fig1, use_container_width=True)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# infra et circ
st.write('## Section 4')
st.subheader("L'infrastructure en fonction du régime de circulation")

infra_labels = {
    '0': '0 – Aucun',
    '1': '1 – Souterrain - tunnel',
    '2': '2 – Pont - autopont',
    '3': '3 – Bretelle d’échangeur ou de raccordement',
    '4': '4 – Voie ferrée',
    '5': '5 – Carrefour aménagé',
    '6': '6 – Zone piétonne',
    '7': '7 – Zone de péage',
    '8': '8 – Chantier',
    '9': '9 – Autres'
}

df_sans_les_non_renseigner['infra'] = df_sans_les_non_renseigner['infra'].astype(
    str)

faire_la_liaison = df_sans_les_non_renseigner.groupby(
    ['infra', 'circ']).size().unstack().reset_index()

faire_la_liaison_melted = pd.melt(
    faire_la_liaison, id_vars='infra', var_name='circ', value_name='Nombre de Trajets')

chart = alt.Chart(faire_la_liaison_melted).mark_bar().encode(
    x=alt.X('infra:O', title='Catégorie d\'infrastructures',
            axis=alt.Axis(labelAngle=0)),
    y=alt.Y('sum(Nombre de Trajets):Q', title='Nombre de Trajets'),
    color=alt.Color('circ:N', title='Régime de circulation',
                    scale=alt.Scale(scheme='category20')),
    order=alt.Order('circ:N')
).properties(width=600, height=400)

st.altair_chart(chart, use_container_width=True)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# lien entre plan et prof on remarque que le plus d'accident c'est avec les routes rectiligne lorsque c plat
st.write('## Section 5')
st.subheader("Le tracé en plan en fonction du profil de déclivité de la route")

plan_labels = {
    1: '1 : Partie rectiligne',
    2: '2 : En courbe à gauche',
    3: '3 : En courbe à droite',
    4: '4 : En « S »'
}

prof_labels = {
    1: '1 : Plat',
    2: '2 : Pente',
    3: '3 : Sommet de côte',
    4: '4 : Bas de côte'
}

faire_la_liaison = df_sans_les_non_renseigner.groupby(
    ['plan', 'prof']).size().unstack().reset_index()
faire_la_liaison_melted = pd.melt(
    faire_la_liaison, id_vars='plan', var_name='prof', value_name='Nombre de Trajets')

fig5 = px.line(faire_la_liaison_melted, x='plan',
               y='Nombre de Trajets', color='prof')
fig5.update_traces(marker_line_width=1)
fig5.update_layout(legend_title_text='Type de Profil')

# Mise à jour des noms de légendes
fig5.for_each_trace(lambda trace: trace.update(
    name=plan_labels.get(int(trace.name), trace.name)))

# Mise à jour des étiquettes de l'axe x
fig5.update_xaxes(ticktext=[plan_labels.get(label, label)
                  for label in faire_la_liaison_melted['plan']], tickvals=faire_la_liaison_melted['plan'])

st.plotly_chart(fig5, use_container_width=True)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# situ et surf
# Vos données et labels
st.write('## Section 6')
st.subheader("La situation de l'accident en fonction de l'état de la surface")

situ_labels = {
    1: '1 : Sur chaussée',
    2: '2 : Sur trottoir',
    3: '3 : Sur piste cyclable',
    4: '4 : Sur accotement',
    5: '5 : Sur bande d’arrêt d’urgence',
    6: '6 : Sur autre voie spéciale',
    7: '7 : Ailleurs'
}

surf_labels = {
    1: '1 : Normale',
    2: '2 : Mouillée',
    3: '3 : Flaque d’eau importante',
    4: '4 : Inondée',
    5: '5 : Enneigée',
    6: '6 : Boue',
    7: '7 : Verglacée',
    8: '8 : Corrodée'
}

faire_la_liaison = df_sans_les_non_renseigner.groupby(
    ['situ', 'surf']).size().unstack().reset_index()
faire_la_liaison_melted = pd.melt(
    faire_la_liaison, id_vars='situ', var_name='surf', value_name='Nombre de Trajets')

line_chart = alt.Chart(faire_la_liaison_melted).mark_line().encode(
    x=alt.X('situ:N', title='Situation', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('sum(Nombre de Trajets):Q', title='Nombre de Trajets'),
    color=alt.Color('surf:N', title='Surface de la chaussée',
                    scale=alt.Scale(scheme='category20'))
).properties(width=600, height=400)

st.altair_chart(line_chart, use_container_width=True)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# entre situ et catr

st.write('## Section 7')
st.subheader("Entre situ et catr")

situ_labels = {
    1: '1 : Sur chaussée',
    2: '2 : Sur trottoir',
    3: '3 : Sur piste cyclable',
    4: '4 : Sur accotement',
    5: '5 : Sur bande d’arrêt d’urgence',
    6: '6 : Sur autre voie spéciale',
    7: '7 : Ailleurs'
}

catr_labels = {
    1: '1 – Autoroute',
    2: '2 – Route nationale',
    3: '3 – Route Départementale',
    4: '4 – Voie Communales',
    5: '5 – Hors réseau public',
    6: '6 – Parc de stationnement ouvert à la circulation publique',
    7: '7 – Routes de métropole urbaine',
    9: '9 – autre'
}

faire_la_liaison = df_sans_les_non_renseigner.groupby(
    ['situ', 'catr']).size().unstack().reset_index()
faire_la_liaison_melted = pd.melt(
    faire_la_liaison, id_vars='situ', var_name='catr', value_name='Nombre de Trajets')

fig7 = px.line(faire_la_liaison_melted, x='situ',
               y='Nombre de Trajets', color='catr')

fig7.update_traces(marker_line_width=1)
fig7.update_layout(legend_title_text='Type de Route')
fig7.update_xaxes(ticktext=[situ_labels.get(label, label)
                  for label in faire_la_liaison_melted['situ']], tickvals=faire_la_liaison_melted['situ'])
st.plotly_chart(fig7, use_container_width=True)

st.write('Pour plus de préicisions')

fig = px.pie(faire_la_liaison_melted, names='catr', values='Nombre de Trajets',
             color_discrete_sequence=px.colors.qualitative.Set3,
             title="Répartition des Types de Route par Situation")
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# vma et catr
st.write('## Section 8')
st.subheader("La catégorie de route en fonction de la vitesse maximale")

vma_labels = {
    0: '0 : Inconnue',
    1: '1 : Moins de 80 km/h',
    2: '2 : 80-90 km/h',
    3: '3 : 100-110 km/h',
    4: '4 : 120-130 km/h',
    5: '5 : 140 km/h ou plus',
}

catr_labels = {
    1: '1 – Autoroute',
    2: '2 – Route nationale',
    3: '3 – Route Départementale',
    4: '4 – Voie Communales',
    5: '5 – Hors réseau public',
    6: '6 – Parc de stationnement ouvert à la circulation publique',
    7: '7 – Routes de métropole urbaine',
    9: '9 – autre'
}

faire_la_liaison = df_sans_les_non_renseigner.groupby(
    ['catr', 'vma']).size().unstack().reset_index()
faire_la_liaison_melted = pd.melt(
    faire_la_liaison, id_vars='catr', var_name='vma', value_name='Nombre de Trajets')

fig = px.box(faire_la_liaison_melted, x='catr', y='Nombre de Trajets', color='vma',
             category_orders={"catr": list(
                 catr_labels.keys()), "vma": list(vma_labels.keys())},
             labels={"catr": "Type de Route", "vma": "Vitesse Maximale Autorisée"})

fig.update_xaxes(type='category')
fig.update_traces(boxpoints='all', jitter=0.3, pointpos=-1.8)
fig.update_yaxes(range=[0, 2000])

st.plotly_chart(fig, use_container_width=True)

st.write("Pour avoir une meilleure visualisation de chaque données : ")

fig = px.box(faire_la_liaison_melted, x='catr', y='Nombre de Trajets', color='vma',
             category_orders={"catr": list(
                 catr_labels.keys()), "vma": list(vma_labels.keys())},
             labels={"catr": "Type de Route", "vma": "Vitesse Maximale Autorisée"})

fig.update_xaxes(type='category')
fig.update_traces(boxpoints='all', jitter=0.3, pointpos=-1.8)
fig.update_yaxes(range=[0, 200])

st.plotly_chart(fig, use_container_width=True)

# Lien
st.markdown(
    """
        ---
        #### Si vous êtes curieux et que vous voulez en apprendre plus sur streamlit 👍, cliquez sur ce lien  :
        - [Liens vers Streamlit](https://streamlit.io)
        """
)

st.markdown(
    """
        ---
        #### Et si vous voulez voir l'actualité des accidents de voitures 😢, cliquez sur ce lien : 
        - [Un accident de voiture](https://www.ouest-france.fr/faits-divers/accidents/)
        """
)

st.markdown("<h2 style='text-align: center;'>😱 Faites bien attention sur la route ! 😱</h2>",
            unsafe_allow_html=True)
