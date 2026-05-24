import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
 
st.set_page_config(
    page_title="Global Gym Analytics",
    page_icon="🏋️",
    layout="wide"
)
 
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0d0d0d;
        color: #f0f0f0;
    }
    .main { background-color: #0d0d0d; }
    h1, h2, h3 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)
 
@st.cache_data
def load_data():
    df = pd.read_csv("clean_gym_data.csv")
    return df
 
df = load_data()
 
st.markdown("<h1 style='font-size:3rem; color:#FFD700;'>🏋️ GLOBAL GYM ANALYTICS</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#aaa; margin-top:-10px;'>Tendencias mundiales de gimnasios y actividad física</p>", unsafe_allow_html=True)
st.markdown("---")
 
# Filtros globales
col1, col2, col3 = st.columns(3)
with col1:
    regions = ["Todas"] + sorted(df["region"].dropna().unique().tolist())
    selected_region = st.selectbox("🌍 Región", regions)
with col2:
    year_min, year_max = int(df["year"].min()), int(df["year"].max())
    year_range = st.slider("📅 Rango de años", year_min, year_max, (year_min, year_max))
with col3:
    top_n = st.selectbox("🏆 Top países", [5, 10, 15, 20], index=1)
 
filtered = df.copy()
if selected_region != "Todas":
    filtered = filtered[filtered["region"] == selected_region]
filtered = filtered[(filtered["year"] >= year_range[0]) & (filtered["year"] <= year_range[1])]
 
# KPIs
st.markdown("<h2 style='color:#FFD700;'>MÉTRICAS CLAVE</h2>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("🏟️ Total Gimnasios", f"{int(filtered['number_of_gyms'].sum()):,}")
with k2:
    st.metric("👥 Membresías Totales", f"{int(filtered['gym_memberships'].sum()):,}")
with k3:
    st.metric("💰 Costo Promedio (USD)", f"${filtered['average_membership_cost_usd'].mean():.1f}")
with k4:
    st.metric("⚖️ Tasa Obesidad Promedio", f"{filtered['obesity_rate'].mean()*100:.1f}%")
 
st.markdown("---")
 
# Gráfico 1: Evolución membresías
st.markdown("<h2 style='color:#FFD700;'>📈 EVOLUCIÓN DE MEMBRESÍAS POR REGIÓN</h2>", unsafe_allow_html=True)
trend = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
trend_grouped = trend.groupby(["year", "region"])["gym_memberships"].sum().reset_index()
fig1 = px.line(trend_grouped, x="year", y="gym_memberships", color="region",
    labels={"gym_memberships": "Membresías", "year": "Año", "region": "Región"},
    color_discrete_sequence=px.colors.qualitative.Bold)
fig1.update_layout(paper_bgcolor="#0d0d0d", plot_bgcolor="#111", font_color="#f0f0f0",
    xaxis=dict(gridcolor="#222"), yaxis=dict(gridcolor="#222"))
st.plotly_chart(fig1, use_container_width=True)
 
# Gráfico 2: Top países
st.markdown("<h2 style='color:#FFD700;'>🏆 TOP PAÍSES POR NÚMERO DE GIMNASIOS</h2>", unsafe_allow_html=True)
top_countries = filtered.groupby("country")["number_of_gyms"].sum().nlargest(top_n).reset_index()
fig2 = px.bar(top_countries, x="number_of_gyms", y="country", orientation="h",
    labels={"number_of_gyms": "Número de Gimnasios", "country": "País"},
    color="number_of_gyms", color_continuous_scale="Inferno")
fig2.update_layout(paper_bgcolor="#0d0d0d", plot_bgcolor="#111", font_color="#f0f0f0",
    yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
st.plotly_chart(fig2, use_container_width=True)
 
# Gráfico 3: Obesidad vs Fitness
st.markdown("<h2 style='color:#FFD700;'>⚖️ OBESIDAD VS PARTICIPACIÓN EN FITNESS</h2>", unsafe_allow_html=True)
scatter_data = filtered.groupby("country").agg({
    "obesity_rate": "mean", "fitness_participation_rate": "mean",
    "gdp_per_capita_usd": "mean", "region": "first"}).reset_index()
fig3 = px.scatter(scatter_data, x="fitness_participation_rate", y="obesity_rate",
    color="region", size="gdp_per_capita_usd", hover_name="country",
    labels={"fitness_participation_rate": "Tasa de Participación en Fitness",
            "obesity_rate": "Tasa de Obesidad", "region": "Región"},
    color_discrete_sequence=px.colors.qualitative.Bold)
fig3.update_layout(paper_bgcolor="#0d0d0d", plot_bgcolor="#111", font_color="#f0f0f0",
    xaxis=dict(gridcolor="#222"), yaxis=dict(gridcolor="#222"))
st.plotly_chart(fig3, use_container_width=True)
 
# Gráfico 4: Ingresos por región
st.markdown("<h2 style='color:#FFD700;'>💵 INGRESOS TOTALES POR REGIÓN</h2>", unsafe_allow_html=True)
revenue = filtered.groupby("region")["total_health_club_revenue_usd"].sum().reset_index()
fig4 = px.pie(revenue, values="total_health_club_revenue_usd", names="region",
    color_discrete_sequence=px.colors.qualitative.Bold, hole=0.4)
fig4.update_layout(paper_bgcolor="#0d0d0d", font_color="#f0f0f0")
st.plotly_chart(fig4, use_container_width=True)
 
st.markdown("---")
 
# NUEVO: Selectbox de país + métricas comparativas
st.markdown("<h2 style='color:#FFD700;'>🔍 ANÁLISIS POR PAÍS</h2>", unsafe_allow_html=True)
 
countries = sorted(df["country"].unique().tolist())
col1, col2 = st.columns(2)
with col1:
    pais1 = st.selectbox("🌐 País 1", countries, index=countries.index("Peru") if "Peru" in countries else 0)
with col2:
    pais2 = st.selectbox("🌐 País 2", countries, index=countries.index("Argentina") if "Argentina" in countries else 1)
 
# Datos de cada país
data_p1 = df[(df["country"] == pais1) & (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
data_p2 = df[(df["country"] == pais2) & (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
 
# Métricas comparativas
st.markdown(f"<h3 style='color:#aaa;'>📊 Comparativa: {pais1} vs {pais2}</h3>", unsafe_allow_html=True)
 
m1, m2, m3, m4 = st.columns(4)
with m1:
    v1 = int(data_p1["number_of_gyms"].sum())
    v2 = int(data_p2["number_of_gyms"].sum())
    st.metric(f"🏟️ Gimnasios {pais1}", f"{v1:,}", delta=f"{v1-v2:,} vs {pais2}")
with m2:
    v1 = int(data_p1["gym_memberships"].sum())
    v2 = int(data_p2["gym_memberships"].sum())
    st.metric(f"👥 Membresías {pais1}", f"{v1:,}", delta=f"{v1-v2:,} vs {pais2}")
with m3:
    v1 = data_p1["obesity_rate"].mean() * 100
    v2 = data_p2["obesity_rate"].mean() * 100
    st.metric(f"⚖️ Obesidad {pais1}", f"{v1:.1f}%", delta=f"{v1-v2:.1f}% vs {pais2}", delta_color="inverse")
with m4:
    v1 = data_p1["gdp_per_capita_usd"].mean()
    v2 = data_p2["gdp_per_capita_usd"].mean()
    st.metric(f"💰 GDP {pais1}", f"${v1:,.0f}", delta=f"${v1-v2:,.0f} vs {pais2}")
 
# Gráfico comparativo evolución
compare_df = df[(df["country"].isin([pais1, pais2])) & 
                (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
fig5 = px.line(compare_df, x="year", y="gym_memberships", color="country",
    title=f"Evolución de Membresías: {pais1} vs {pais2}",
    labels={"gym_memberships": "Membresías", "year": "Año", "country": "País"},
    color_discrete_sequence=["#FFD700", "#00BFFF"])
fig5.update_layout(paper_bgcolor="#0d0d0d", plot_bgcolor="#111", font_color="#f0f0f0",
    xaxis=dict(gridcolor="#222"), yaxis=dict(gridcolor="#222"))
st.plotly_chart(fig5, use_container_width=True)
 
st.markdown("---")
st.markdown("<p style='color:#555; text-align:center;'>Global Gym Analytics Dashboard • Datos: clean_gym_data.csv</p>", unsafe_allow_html=True)
