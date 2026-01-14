import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style/main.css")


DB_PATH = "database.db"

@st.cache_data
def load_aggregated_data():
    """
    Charge les données agrégées depuis la base de données SQLite.
    """
    conn = sqlite3.connect(DB_PATH)
    encours_par_produit = pd.read_sql_query("SELECT * FROM agg_encours_par_produit", conn)
    repartition_agences = pd.read_sql_query("SELECT * FROM agg_repartition_agences", conn)
    perf_gestionnaire = pd.read_sql_query("SELECT * FROM agg_perf_gestionnaire", conn)
    top_deposants = pd.read_sql_query("SELECT * FROM agg_top_deposants", conn)
    conn.close()
    return encours_par_produit, repartition_agences, perf_gestionnaire, top_deposants

encours_par_produit, repartition_agences, perf_gestionnaire, top_deposants = load_aggregated_data()


st.title("Dashboard de Suivi Client")
st.markdown("Analyse des comptes, performances et répartitions.")


total_encours_top10 = top_deposants['Total Encours'].sum()
total_encours_total = repartition_agences['montant'].sum()
concentration_risk = (total_encours_top10 / total_encours_total) * 100 if total_encours_total else 0

st.markdown('<div class="card">', unsafe_allow_html=True)
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="Encours Total", value=f"{total_encours_total:,.0f} €")
with kpi2:
    st.metric(label="Encours Top 10 Déposants", value=f"{total_encours_top10:,.0f} €")
with kpi3:
    st.metric(label="Taux de Concentration", value=f"{concentration_risk:.2f} %")
st.markdown('</div>', unsafe_allow_html=True)



col1, col2 = st.columns(2)

PLOTLY_TEMPLATE = "seaborn"
COLOR_SEQUENCE = px.colors.qualitative.Set2

with col1:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Répartition par Produit")
    fig_produit = px.pie(encours_par_produit,
                         values='AvailableBalance',
                         names='nom_produit',
                         hole=0.6,
                         template=PLOTLY_TEMPLATE,
                         color_discrete_sequence=COLOR_SEQUENCE)
    fig_produit.update_traces(textposition='outside', textinfo='percent+label', hovertemplate="<b>%{label}</b><br>Encours: %{value:,.0f} €<br>(%{percent})")
    fig_produit.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_produit, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Performance par Gestionnaire")
    fig_gestionnaire = make_subplots(specs=[[{"secondary_y": True}]])
    fig_gestionnaire.add_trace(
        go.Bar(x=perf_gestionnaire['gestionnaire'], y=perf_gestionnaire['montant'], name='Encours de dépôt', marker_color=COLOR_SEQUENCE[0]),
        secondary_y=False,
    )
    fig_gestionnaire.add_trace(
        go.Scatter(x=perf_gestionnaire['gestionnaire'], y=perf_gestionnaire['nombre_de_compte'], name='Nombre de comptes', mode='lines+markers', line=dict(color=COLOR_SEQUENCE[1])),
        secondary_y=True,
    )
    fig_gestionnaire.update_layout(
        template=PLOTLY_TEMPLATE,
        xaxis_title="Gestionnaire",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_gestionnaire.update_yaxes(title_text="Encours de dépôt (€)", secondary_y=False)
    fig_gestionnaire.update_yaxes(title_text="Nombre de comptes", secondary_y=True)
    st.plotly_chart(fig_gestionnaire, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Répartition par Agence")
    fig_agences = make_subplots(specs=[[{"secondary_y": True}]])
    fig_agences.add_trace(
        go.Bar(x=repartition_agences['nom_agence'], y=repartition_agences['montant'], name='Encours (Montant)', marker_color=COLOR_SEQUENCE[2]),
        secondary_y=False,
    )
    fig_agences.add_trace(
        go.Scatter(x=repartition_agences['nom_agence'], y=repartition_agences['nombre_de_compte'], name='Nombre de comptes', mode='lines+markers', line=dict(color=COLOR_SEQUENCE[3])),
        secondary_y=True,
    )
    fig_agences.update_layout(
        template=PLOTLY_TEMPLATE,
        xaxis_title="Agence",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_agences.update_yaxes(title_text="Encours (€)", secondary_y=False)
    fig_agences.update_yaxes(title_text="Nombre de comptes", secondary_y=True)
    st.plotly_chart(fig_agences, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Top 10 Déposants")


    display_deposants = top_deposants.copy()
    display_deposants['Total Encours'] = display_deposants['Total Encours'].map('{:,.0f} €'.format)
    st.dataframe(display_deposants, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
