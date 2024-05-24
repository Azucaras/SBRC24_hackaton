import requests
import time 
import json
import numpy as np
import pandas as pd
import streamlit as st 
import plotly.express as px
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from streamlit_autorefresh import st_autorefresh
import folium
import webbrowser


# response = requests.get("http://localhost:8080/inspect/probabilities")
# payload = response.json()["reports"][0]["payload"]
# bytes.fromhex(payload[2:]).decode('utf-8')

        # if payload_str == "probabilities":
        #     result = json.dumps(probabilities).encode('utf-8').hex()



dm = pd.read_json("/home/vicente/seila/dados.json")
ds = pd.read_json("/home/vicente/seila/salvamento.json")

st.set_page_config(
    page_title="", 
    page_icon='✅', 
    layout="wide", 
    initial_sidebar_state="expanded")

st_autorefresh(interval=5, limit = 100, key="fizzbuzzcounter")

st.title("GBB → GeoGuardBlock")

# Criando sidebar
with st.sidebar:
    # logo_url = '~/vicente/seila/logo.png'
    # st.sidebar.image(logo_url, width=200)
    st.title("Tipos de gráfico")
    opcoes = ("Gráfico de linha", "Mapa", "Mapa de ocorrência")
    select_option = st.sidebar.selectbox("Selecione uma opção", opcoes)

#Criando espaço na pagina
placeholder = st.empty()

for seconds in range(500):
    dm["reported_time"] = pd.to_datetime(dm["reported_time"])
    dm['hora'] = dm['reported_time'].dt.hour
    avg_prob = dm.groupby('hora')['probability'].mean()

    with placeholder.container():
        fig1, fig2 = st.columns(2)
        with fig1:
            st.markdown('### Probabilidade de ocorrência de desastres por hora')
            fig = px.line(avg_prob, x=avg_prob.index, y=avg_prob.values, width=600, height=400, labels={'x':'Hora', 'y':'Probabilidade'})
            st.write(fig)
        st.markdown('### Tabela de probalidade de ocorrência de desastres por região')
        table = st.table(ds)
        with fig2:
            st.markdown('### Mapa de ocorrência de desastres')
            fig = px.scatter_mapbox(dm, lat=dm["lat"], lon=dm["long"], color=dm["probability"], size=dm["probability"], zoom=11, mapbox_style="open-street-map")
            st.write(fig)
        st.markdown('### Tabela de ocorrência de desastres')
        tabela = st.table(dm)

placeholder = st.empty()
