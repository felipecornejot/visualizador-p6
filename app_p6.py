import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import requests

# --- Paleta de Colores ---
# Definición de colores en formato RGB (0-1) para Matplotlib
color_primario_1_rgb = (14/255, 69/255, 74/255) # 0E454A (Oscuro)
color_primario_2_rgb = (31/255, 255/255, 95/255) # 1FFF5F (Verde vibrante)
color_primario_3_rgb = (255/255, 255/255, 255/255) # FFFFFF (Blanco)

# Colores del logo de Sustrend para complementar
color_sustrend_1_rgb = (0/255, 155/255, 211/255) # 009BD3 (Azul claro)
color_sustrend_2_rgb = (0/255, 140/255, 207/255) # 008CCF (Azul medio)
color_sustrend_3_rgb = (0/255, 54/255, 110/255) # 00366E (Azul oscuro)

# Selección de colores para los gráficos
colors_for_charts = [color_primario_1_rgb, color_primario_2_rgb, color_sustrend_1_rgb, color_sustrend_3_rgb]

# --- Configuración de la página de Streamlit ---
st.set_page_config(layout="wide")

st.title('✨ Visualizador de Impactos - Proyecto P6')
st.subheader('Valorización de descartes cárnicos')
st.markdown("""
    Ajusta los parámetros para explorar cómo las proyecciones de impacto ambiental y económico del proyecto
    varían con diferentes escenarios de volumen de descartes procesados, tasa de valorización, y precio de los péptidos.
""")

# --- Widgets Interactivos para Parámetros (Streamlit) ---
st.sidebar.header('Parámetros de Simulación')

descartes_procesados = st.sidebar.slider(
    'Descartes cárnicos procesados (ton/año):',
    min_value=10,
    max_value=100,
    value=50,
    step=5,
    help="Volumen anual de descartes cárnicos procesados."
)

tasa_valorizacion = st.sidebar.slider(
    'Tasa de valorización (%):',
    min_value=0.70, # Corregido a float para el slider
    max_value=0.90, # Corregido a float para el slider
    value=0.85,
    step=0.01,
    format='%.1f%%', # Formato para mostrar como porcentaje
    help="Porcentaje de descartes que se transforman en péptidos funcionales."
)

factor_gei_transporte = st.sidebar.slider(
    'Factor GEI transporte evitado (tCO₂e/5 ton):',
    min_value=1.0,
    max_value=2.0,
    value=1.2,
    step=0.1,
    help="Factor de emisiones de GEI evitadas por transporte por cada 5 toneladas de péptidos."
)

precio_peptidos = st.sidebar.slider(
    'Precio de mercado péptidos (USD/ton):',
    min_value=5000,
    max_value=10000,
    value=8000,
    step=500,
    help="Precio de mercado estimado para los péptidos funcionales."
)

# --- Cálculos de Indicadores ---
peptidos_producidos = descartes_procesados * tasa_valorizacion
gei_ev_transporte = (peptidos_producidos / 5) * factor_gei_transporte
ingresos_generados = peptidos_producidos * precio_peptidos
ahorro_aditivos = peptidos_producidos * 0.2 # suponemos 20% sustitución
alianzas_comerciales = 2 # Valor fijo según ficha

st.header('Resultados Proyectados Anuales:')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="🧪 **Péptidos funcionales obtenidos**", value=f"{peptidos_producidos:.2f} ton/año")
    st.caption("Cantidad de péptidos naturales obtenidos a partir de descartes cárnicos.")
with col2:
    st.metric(label="🌎 **GEI evitados por transporte**", value=f"{gei_ev_transporte:.2f} tCO₂e/año")
    st.caption("Reducción de emisiones de gases de efecto invernadero por el transporte.")
with col3:
    st.metric(label="💰 **Ingresos generados**", value=f"USD {ingresos_generados:,.2f}")
    st.caption("Ingresos económicos por la venta de péptidos funcionales.")

col4, col5 = st.columns(2)

with col4:
    st.metric(label="🌱 **Aditivos sintéticos reemplazados**", value=f"{ahorro_aditivos:.2f} ton/año")
    st.caption("Cantidad de aditivos sintéticos sustituidos por los péptidos naturales.")
with col5:
    st.metric(label="🤝 **Alianzas comerciales**", value=f"{alianzas_comerciales}")
    st.caption("Número de acuerdos de simbiosis industrial.")

st.markdown("---")

st.header('📊 Análisis Gráfico de Impactos')

# --- Visualización (Gráficos 2D con Matplotlib) ---
# Datos línea base (según ficha P6)
base_peptidos = 8.5
base_gei = 1.2
base_ingresos = 1600

# Creamos una figura con 3 subplots (2D)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7), facecolor=color_primario_3_rgb)
fig.patch.set_facecolor(color_primario_3_rgb)

# Definición de etiquetas y valores para los gráficos de barras 2D
labels = ['Línea Base', 'Proyección']
bar_width = 0.6
x = np.arange(len(labels))

# --- Gráfico 1: GEI Evitados (tCO₂e/año) ---
gei_values = [base_gei, gei_ev_transporte]
bars1 = ax1.bar(x, gei_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax1.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax1.set_title('GEI Evitados por Transporte', fontsize=14, color=colors_for_charts[3], pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax1.yaxis.set_tick_params(colors=colors_for_charts[0])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(axis='x', length=0)
max_gei_val = max(gei_values)
ax1.set_ylim(bottom=0, top=max(max_gei_val * 1.15, 1))
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, round(yval, 2), ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 2: Péptidos Producidos (ton/año) ---
peptidos_values = [base_peptidos, peptidos_producidos]
bars2 = ax2.bar(x, peptidos_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax2.set_ylabel('Toneladas/año', fontsize=12, color=colors_for_charts[0])
ax2.set_title('Péptidos Producidos', fontsize=14, color=colors_for_charts[3], pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax2.yaxis.set_tick_params(colors=colors_for_charts[0])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(axis='x', length=0)
max_peptidos_val = max(peptidos_values)
ax2.set_ylim(bottom=0, top=max(max_peptidos_val * 1.15, 1))
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, round(yval, 2), ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 3: Ingresos Generados (USD/año) ---
ingresos_values = [base_ingresos, ingresos_generados]
bars3 = ax3.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax3.set_ylabel('USD/año', fontsize=12, color=colors_for_charts[3])
ax3.set_title('Ingresos Generados', fontsize=14, color=colors_for_charts[3], pad=20)
ax3.set_xticks(x)
ax3.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax3.yaxis.set_tick_params(colors=colors_for_charts[0])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.tick_params(axis='x', length=0)
max_ingresos_val = max(ingresos_values)
ax3.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000))
for bar in bars3:
    yval = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"${yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
st.pyplot(fig)

# --- Funcionalidad de descarga de cada gráfico ---
st.markdown("---")
st.subheader("Descargar Gráficos Individualmente")

# Función auxiliar para generar el botón de descarga
def download_button(fig, filename_prefix, key):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button(
        label=f"Descargar {filename_prefix}.png",
        data=buf.getvalue(),
        file_name=f"{filename_prefix}.png",
        mime="image/png",
        key=key
    )

# Crear figuras individuales para cada gráfico para poder descargarlas
# Figura 1: GEI Evitados
fig_gei, ax_gei = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_gei.bar(x, gei_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax_gei.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax_gei.set_title('GEI Evitados por Transporte', fontsize=14, color=colors_for_charts[3], pad=20)
ax_gei.set_xticks(x)
ax_gei.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_gei.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_gei.spines['top'].set_visible(False)
ax_gei.spines['right'].set_visible(False)
ax_gei.tick_params(axis='x', length=0)
ax_gei.set_ylim(bottom=0, top=max(max_gei_val * 1.15, 1))
for bar in ax_gei.patches:
    yval = bar.get_height()
    ax_gei.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, round(yval, 2), ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_gei, "GEI_Evitados", "download_gei")
plt.close(fig_gei)

# Figura 2: Péptidos Producidos
fig_peptidos, ax_peptidos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_peptidos.bar(x, peptidos_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax_peptidos.set_ylabel('Toneladas/año', fontsize=12, color=colors_for_charts[0])
ax_peptidos.set_title('Péptidos Producidos', fontsize=14, color=colors_for_charts[3], pad=20)
ax_peptidos.set_xticks(x)
ax_peptidos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_peptidos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_peptidos.spines['top'].set_visible(False)
ax_peptidos.spines['right'].set_visible(False)
ax_peptidos.tick_params(axis='x', length=0)
ax_peptidos.set_ylim(bottom=0, top=max(max_peptidos_val * 1.15, 1))
for bar in ax_peptidos.patches:
    yval = bar.get_height()
    ax_peptidos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, round(yval, 2), ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_peptidos, "Peptidos_Producidos", "download_peptidos")
plt.close(fig_peptidos)

# Figura 3: Ingresos Generados
fig_ingresos, ax_ingresos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_ingresos.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax_ingresos.set_ylabel('USD/año', fontsize=12, color=colors_for_charts[3])
ax_ingresos.set_title('Ingresos Generados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_ingresos.set_xticks(x)
ax_ingresos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_ingresos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_ingresos.spines['top'].set_visible(False)
ax_ingresos.spines['right'].set_visible(False)
ax_ingresos.tick_params(axis='x', length=0)
ax_ingresos.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000))
for bar in ax_ingresos.patches:
    yval = bar.get_height()
    ax_ingresos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"${yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_ingresos, "Ingresos_Generados", "download_ingresos")
plt.close(fig_ingresos)

st.markdown("---")
st.markdown("### Información Adicional:")
st.markdown(f"- **Estado de Avance y Recomendaciones:** El proyecto ha logrado validar técnicamente la obtención de péptidos naturales a partir de descartes avícolas en condiciones controladas de laboratorio. Se encuentran en desarrollo acuerdos de colaboración con actores de la industria avícola para escalar el proceso a nivel piloto, y se está explorando el interés comercial de empresas elaboradoras de productos cárnicos.")

st.markdown("---")
# Texto de atribución centrado
st.markdown("<div style='text-align: center;'>Visualizador Creado por el equipo Sustrend SpA en el marco del Proyecto TT GREEN Foods</div>", unsafe_allow_html=True)

# Aumentar el espaciado antes de los logos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Mostrar Logos ---
col_logos_left, col_logos_center, col_logos_right = st.columns([1, 2, 1])

with col_logos_center:
    sustrend_logo_url = "https://drive.google.com/uc?id=1vx_znPU2VfdkzeDtl91dlpw_p9mmu4dd"
    ttgreenfoods_logo_url = "https://drive.google.com/uc?id=1uIQZQywjuQJz6Eokkj6dNSpBroJ8tQf8"

    try:
        sustrend_response = requests.get(sustrend_logo_url)
        sustrend_response.raise_for_status()
        sustrend_image = Image.open(BytesIO(sustrend_response.content))

        ttgreenfoods_response = requests.get(ttgreenfoods_logo_url)
        ttgreenfoods_response.raise_for_status()
        ttgreenfoods_image = Image.open(BytesIO(ttgreenfoods_response.content))

        st.image([sustrend_image, ttgreenfoods_image], width=100)
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar los logos desde las URLs. Por favor, verifica los enlaces: {e}")
    except Exception as e:
        st.error(f"Error inesperado al procesar las imágenes de los logos: {e}")

st.markdown("<div style='text-align: center; font-size: small; color: gray;'>Viña del Mar, Valparaíso, Chile</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align: center; font-size: smaller; color: gray;'>Versión del Visualizador: 1.8</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='text-align: center; font-size: x-small; color: lightgray;'>Desarrollado con Streamlit</div>", unsafe_allow_html=True)
