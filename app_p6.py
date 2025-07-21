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

st.title('✨ Visualizador de Impactos - Proyecto P5')
st.subheader('Insect Based Food: Producción de proteína alternativa a partir de insectos')
st.markdown("""
    Ajusta los parámetros para explorar las proyecciones de impacto ambiental y económico del proyecto P5,
    que busca valorizar residuos orgánicos para producir proteína alternativa a partir de insectos.
""")

# --- 1. Datos del Proyecto (Línea Base) ---
# Datos línea base (según ficha, los valores del script original para la "Línea Base")
base_gei_evitados_total = 10  # tCO₂e/año (ejemplo del script original)
base_residuos_valorizados = 15  # ton/año (ejemplo del script original)
base_ingresos_estimados = 2000 # USD/año (ejemplo del script original)

# --- 2. Widgets Interactivos para Parámetros (Streamlit) ---
st.sidebar.header('Parámetros de Simulación')

residuos_procesados = st.sidebar.slider(
    'Residuos Procesados (ton/año):',
    min_value=5,
    max_value=50,
    value=15,
    step=5,
    help="Cantidad de residuos orgánicos procesados anualmente para la producción de proteína de insectos."
)

tasa_aprovechamiento = st.sidebar.slider(
    'Tasa de Aprovechamiento (%):',
    min_value=0.5,
    max_value=0.9,
    value=0.8,
    step=0.05,
    format='%.1f%%',
    help="Porcentaje de los residuos procesados que se transforman efectivamente en biomasa proteica valorizada."
)

factor_gei_relleno = st.sidebar.slider(
    'Factor GEI Relleno Sanitario (tCO₂e/ton):',
    min_value=0.4,
    max_value=0.6,
    value=0.52,
    step=0.01,
    help="Factor de emisión de GEI asociado a la disposición de residuos orgánicos en rellenos sanitarios."
)

factor_gei_sustitucion = st.sidebar.slider(
    'Factor GEI Sustitución Proteína (tCO₂e/ton):',
    min_value=1.5,
    max_value=2.5,
    value=2.0,
    step=0.1,
    help="Factor de GEI evitado por la sustitución de proteína convencional (ej. carne, soya importada) por proteína de insectos."
)

precio_proteina = st.sidebar.slider(
    'Precio Proteína Equivalente (USD/ton):',
    min_value=1000,
    max_value=3000,
    value=2000,
    step=100,
    help="Precio estimado de la tonelada de proteína de insectos en el mercado, en relación con proteínas que sustituye."
)

# --- 3. Cálculos de Indicadores ---
residuos_valorizados = residuos_procesados * tasa_aprovechamiento
gei_ev_relleno = residuos_procesados * factor_gei_relleno
gei_ev_sustitucion = residuos_valorizados * factor_gei_sustitucion
ingresos_estimados = residuos_valorizados * precio_proteina
empleos_generados = 2 # Fijo según el script original
interacciones_cadena = 3 # Fijo según el script original

st.header('Resultados Proyectados Anuales:')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="♻️ **Residuos Orgánicos Valorizados**", value=f"{residuos_valorizados:.2f} ton")
    st.caption("Cantidad de residuos orgánicos transformados en biomasa útil.")
with col2:
    st.metric(label="🌎 **GEI Evitados en Relleno Sanitario**", value=f"{gei_ev_relleno:.2f} tCO₂e")
    st.caption("Reducción de emisiones por desvío de residuos de rellenos sanitarios.")
with col3:
    st.metric(label="🥩 **GEI Evitados por Sustitución Proteína**", value=f"{gei_ev_sustitucion:.2f} tCO₂e")
    st.caption("Reducción de emisiones por reemplazar proteínas convencionales.")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(label="💰 **Ingresos Estimados**", value=f"USD {ingresos_estimados:,.2f}")
    st.caption("Valor económico generado por la venta de la proteína de insectos.")
with col5:
    st.metric(label="🧑‍🤝‍🧑 **Empleos Generados**", value=f"{empleos_generados}")
    st.caption("Número de empleos directos generados por la operación.")
with col6:
    st.metric(label="🔗 **Interacciones Cadena Suministro**", value=f"{interacciones_cadena}")
    st.caption("Colaboraciones con actores de la cadena de suministro circular.")

st.markdown("---")

st.header('📊 Análisis Gráfico de Impactos')

# --- Visualización (Gráficos 2D con Matplotlib) ---
labels = ['Línea Base', 'Proyección']
bar_width = 0.6
x = np.arange(len(labels))

# Creamos una figura con 3 subplots (2D)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7), facecolor=color_primario_3_rgb)
fig.patch.set_facecolor(color_primario_3_rgb)

# --- Gráfico 1: GEI Evitados Total (tCO₂e/año) ---
# Suma de GEI evitados del relleno sanitario y por sustitución de proteína
gei_evitados_total_proyeccion = gei_ev_relleno + gei_ev_sustitucion
gei_values = [base_gei_evitados_total, gei_evitados_total_proyeccion]
bars1 = ax1.bar(x, gei_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax1.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax1.set_title('GEI Evitados Total', fontsize=14, color=colors_for_charts[3], pad=20)
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
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 2: Residuos Valorizados (ton/año) ---
residuos_values = [base_residuos_valorizados, residuos_valorizados]
bars2 = ax2.bar(x, residuos_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax2.set_ylabel('Toneladas/año', fontsize=12, color=colors_for_charts[0])
ax2.set_title('Residuos Orgánicos Valorizados', fontsize=14, color=colors_for_charts[3], pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax2.yaxis.set_tick_params(colors=colors_for_charts[0])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(axis='x', length=0)
max_residuos_val = max(residuos_values)
ax2.set_ylim(bottom=0, top=max(max_residuos_val * 1.15, 1))
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 3: Ingresos Estimados (USD/año) ---
ingresos_values = [base_ingresos_estimados, ingresos_estimados]
bars3 = ax3.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax3.set_ylabel('USD/año', fontsize=12, color=colors_for_charts[3])
ax3.set_title('Ingresos Estimados', fontsize=14, color=colors_for_charts[3], pad=20)
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
    ax3.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"${yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])

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
# Figura 1: GEI Evitados Total
fig_gei, ax_gei = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_gei.bar(x, gei_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax_gei.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax_gei.set_title('GEI Evitados Total', fontsize=14, color=colors_for_charts[3], pad=20)
ax_gei.set_xticks(x)
ax_gei.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_gei.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_gei.spines['top'].set_visible(False)
ax_gei.spines['right'].set_visible(False)
ax_gei.tick_params(axis='x', length=0)
ax_gei.set_ylim(bottom=0, top=max(max_gei_val * 1.15, 1))
for bar in ax_gei.patches:
    yval = bar.get_height()
    ax_gei.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_gei, "GEI_Evitados_Total", "download_gei")
plt.close(fig_gei)

# Figura 2: Residuos Valorizados
fig_residuos, ax_residuos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_residuos.bar(x, residuos_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax_residuos.set_ylabel('Toneladas/año', fontsize=12, color=colors_for_charts[0])
ax_residuos.set_title('Residuos Orgánicos Valorizados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_residuos.set_xticks(x)
ax_residuos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_residuos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_residuos.spines['top'].set_visible(False)
ax_residuos.spines['right'].set_visible(False)
ax_residuos.tick_params(axis='x', length=0)
ax_residuos.set_ylim(bottom=0, top=max(max_residuos_val * 1.15, 1))
for bar in ax_residuos.patches:
    yval = bar.get_height()
    ax_residuos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_residuos, "Residuos_Valorizados", "download_residuos")
plt.close(fig_residuos)

# Figura 3: Ingresos Estimados
fig_ingresos, ax_ingresos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_ingresos.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax_ingresos.set_ylabel('USD/año', fontsize=12, color=colors_for_charts[3])
ax_ingresos.set_title('Ingresos Estimados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_ingresos.set_xticks(x)
ax_ingresos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_ingresos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_ingresos.spines['top'].set_visible(False)
ax_ingresos.spines['right'].set_visible(False)
ax_ingresos.tick_params(axis='x', length=0)
ax_ingresos.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000))
for bar in ax_ingresos.patches:
    yval = bar.get_height()
    ax_ingresos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"${yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_ingresos, "Ingresos_Estimados", "download_ingresos")
plt.close(fig_ingresos)

st.markdown("---")
st.markdown("### Información Adicional:")
st.markdown("""
- **Estado de Avance y Recomendaciones:** El proyecto P5 se encuentra en una etapa avanzada de validación de laboratorio, con resultados positivos en la calidad nutricional del producto final y la eficiencia de la tecnología para transformar residuos orgánicos en biomasa proteica. Se recomienda profundizar en la caracterización de los residuos valorizados, cuantificar su origen y tipo, y formalizar protocolos de recolección y manejo.
- **Monitoreo de Impactos:** Se sugiere establecer un sistema de monitoreo de emisiones GEI evitadas (por reducción de disposición en relleno sanitario y sustitución de insumos de alto impacto), e integrar métricas de uso de agua y energía.
- **Alianzas Estratégicas:** Se recomienda fomentar acuerdos con municipios, agroindustrias y comercios locales para el abastecimiento regular de residuos orgánicos y el desarrollo de una cadena de suministro circular.
- **Evaluación Económica:** Incluir una evaluación económica ex ante con métricas como VAN y TIR para dimensionar el potencial de escalamiento comercial y los requerimientos de inversión inicial.
""")

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
st.sidebar.markdown(f"<div style='text-align: center; font-size: smaller; color: gray;'>Versión del Visualizador: 1.0</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='text-align: center; font-size: x-small; color: lightgray;'>Desarrollado con Streamlit</div>", unsafe_allow_html=True)
