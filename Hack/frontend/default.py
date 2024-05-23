import time 
import json
import numpy as np
import pandas as pd
import streamlit as st 
import plotly.express as px
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from streamlit_autorefresh import st_autorefresh

dm = pd.read_json("~/Hack/dados.json")

st.set_page_config(
    page_title="Projeto Hackaton 2024 - Temporário", 
    page_icon='✅', 
    layout="wide", 
    initial_sidebar_state="expanded")

st_autorefresh(interval=5, limit = 100, key="fizzbuzzcounter")

st.title("Projeto Hackaton 2024 - Temporário")

# Criando sidebar
with st.sidebar:
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
        with fig2:
            st.markdown('### Mapa de ocorrência de desastres')
            fig = px.scatter_mapbox(dm, lat=dm["lat"], lon=dm["long"], color=dm["probability"], size=dm["probability"], zoom=13, mapbox_style="open-street-map")
            st.write(fig)

placeholder = st.empty()



# if avg_prob.values.max() > 0.4:
#     st.warning("Alerta → Possível estado crítico de desastre!")
# else:
#     st.success("Tudo sob controle!")


# if st.warning:
#     if st.button("Ignorar alerta"):
#         st.warning = False
#         st.write("Alerta ignorado!")
        











# <template>
#   <v-app>
#     <v-app-bar :elevation="1">
#       <template #prepend></template>
#       <v-spacer></v-spacer>
#       <span>
#         <v-icon icon="mdi:mdi-vuetify"></v-icon>
#         <b> Nuxt.js Template</b>
#       </span>
#       <v-spacer></v-spacer>
#     </v-app-bar>

#     <v-main>
#       <slot></slot>
#     </v-main>

#     <v-footer app border>
#       This is a footer! @ {{ new Date().getFullYear() }}
#     </v-footer>
#   </v-app>
# </template>



# <!-- 
# <template>
#   <v-layout>
#     <v-app-bar :elevation="1">
#       <template #prepend>
#         <nuxt-link to="/">
#           <v-img height="50px" width="100px" src="/logo.svg" alt="Logo" />
#         </nuxt-link>
#       </template>
#       <v-app-bar-title>Integra Chagas</v-app-bar-title>
#       <v-spacer></v-spacer>
#       <v-btn
#         v-for="navItem in navigation"
#         :key="navItem.title"
#         active-class="navbar-active-link"
#         :to="navItem.href"
#         :ripple="false"
#         variant="plain"
#       >
#         {{ navItem.title }}
#       </v-btn>
#       <v-btn
#         v-if="$store.getToken"
#         active-class="navbar-active-link"
#         :ripple="false"
#         variant="plain"
#         @click.prevent="logout"
#       >
#         {{ $store.getUsername }}&nbsp;<v-icon>mdi-logout</v-icon>
#       </v-btn>
#     </v-app-bar>

#     <v-main>
#       <slot></slot>
#     </v-main>

# <v-footer app border style="display: relative">
#       This is a footer! @ {{ new Date().getFullYear() }}
#     </v-footer> -->
#   <!-- </v-layout>
# </template>

# <script setup>
# // Pinia storage
# const { $store } = useNuxtApp();

# // Nuxt router
# const router = useRouter();

# const navigation = ref([
#   {
#     title: "Formularios",
#     href: "/",
#   },
# ]);

# function logout() {
#   $store.resetToken();
#   router.push("/");
# }
# </script>

# <style>
# .v-btn-title {
#   text-transform: uppercase !important;
#   font-size: medium !important;
# }

# .navbar-active-link .v-btn-title {
#   text-decoration: underline !important;
#   font-weight: bold !important;
# }
# </style> --> 
