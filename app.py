import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ── Configuração da página ──────────────────────────────────────────
st.set_page_config(
    page_title="Sales Dashboard · Superstore",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS customizado ─────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fundo geral */
    .stApp { background-color: #F5F7FA; }

    /* Sidebar fundo */
    section[data-testid="stSidebar"] {
        background-color: #1E3A5F;
        padding-top: 20px;
    }

    /* Sidebar textos */
    section[data-testid="stSidebar"] * {
        color: #F9FAFB !important;
    }

    /* Sidebar título */
    section[data-testid="stSidebar"] h2 {
        color: white !important;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 0.04em;
    }

    /* Labels dos filtros */
    section[data-testid="stSidebar"] label {
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: #93C5FD !important;
    }

    /* Caixa do multiselect */
    section[data-testid="stSidebar"] .stMultiSelect > div > div {
        background-color: #1F3A5F !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 8px !important;
        color: white !important;
    }

    /* Tags selecionadas */
    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #2563EB !important;
        border-radius: 6px !important;
        color: white !important;
        font-size: 12px !important;
    }

    /* Dropdown do multiselect */
    div[data-baseweb="popover"] {
        background-color: #1E3A5F !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="popover"] li {
        color: #F9FAFB !important;
        font-size: 13px !important;
    }
    div[data-baseweb="popover"] li:hover {
        background-color: #2563EB !important;
    }

    /* Divisor da sidebar */
    section[data-testid="stSidebar"] hr {
        border-color: #3B82F6 !important;
        opacity: 0.3;
    }

    /* Cards de KPI */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border-left: 5px solid #3B82F6;
    }
    .kpi-label {
        font-size: 13px;
        color: #6B7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
    }
    .kpi-card.green { border-left-color: #10B981; }
    .kpi-card.purple { border-left-color: #8B5CF6; }

    /* Títulos de seção */
    .section-title {
        font-size: 15px;
        font-weight: 700;
        color: #374151;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin: 28px 0 12px 0;
        padding-bottom: 6px;
        border-bottom: 2px solid #E5E7EB;
    }

    /* Cabeçalho */
    .header-box {
        background: linear-gradient(135deg, #1E3A5F 0%, #2563EB 100%);
        border-radius: 14px;
        padding: 28px 36px;
        margin-bottom: 24px;
        color: white;
    }
    .header-box h1 {
        color: white !important;
        font-size: 26px;
        font-weight: 800;
        margin: 0;
    }
   .header-box p {
        color: #BFDBFE !important;
        font-size: 14px;
        margin: 4px 0 0 0;
    }

    /* Tabela de dados */
    .stDataFrame {
        background-color: white !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
    .stDataFrame iframe {
        background-color: white !important;
    }

    /* Expander */
    div[data-testid="stExpander"] {
        background-color: white !important;
        border-radius: 12px !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    div[data-testid="stExpander"] summary {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Carregar dados ───────────────────────────────────────────────────
@st.cache_data
def carregar_dados():
    df = pd.read_csv('data/Sample - Superstore.csv', encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.to_period('M')
    return df

df = carregar_dados()

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗂 Filtros")
    st.markdown("---")

    anos = sorted(df['Year'].unique())
    ano_selecionado = st.multiselect("📅 Ano", anos, default=anos)

    regioes = sorted(df['Region'].unique())
    regiao_selecionada = st.multiselect("🌎 Região", regioes, default=regioes)

    categorias = sorted(df['Category'].unique())
    categoria_selecionada = st.multiselect("📦 Categoria", categorias, default=categorias)

    st.markdown("---")
    st.markdown("**📊 Sales Dashboard**")
    st.markdown("Superstore Dataset · Kaggle")

# ── Filtrar dados ────────────────────────────────────────────────────
df_f = df[
    (df['Year'].isin(ano_selecionado)) &
    (df['Region'].isin(regiao_selecionada)) &
    (df['Category'].isin(categoria_selecionada))
]

# ── Cabeçalho ────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1>📊 Sales Dashboard — Superstore</h1>
    <p>Análise exploratória de vendas · Use os filtros na barra lateral para explorar os dados</p>
</div>
""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">💰 Total de Vendas</div>
        <div class="kpi-value">$ {df_f['Sales'].sum():,.0f}</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-label">📈 Total de Lucro</div>
        <div class="kpi-value">$ {df_f['Profit'].sum():,.0f}</div>
    </div>""", unsafe_allow_html=True)

with k3:
    margem = (df_f['Profit'].sum() / df_f['Sales'].sum() * 100) if df_f['Sales'].sum() > 0 else 0
    st.markdown(f"""
    <div class="kpi-card purple">
        <div class="kpi-label">📉 Margem de Lucro</div>
        <div class="kpi-value">{margem:.1f}%</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color:#F59E0B">
        <div class="kpi-label">🧾 Total de Pedidos</div>
        <div class="kpi-value">{df_f['Order ID'].nunique():,}</div>
    </div>""", unsafe_allow_html=True)

# ── Paleta e estilo dos gráficos ─────────────────────────────────────
CORES = ["#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
sns.set_style("whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.4,
})

# ── Linha 1: Vendas por Categoria + Lucro por Região ─────────────────
st.markdown('<div class="section-title">Desempenho por Categoria e Região</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    with st.container():
        vendas_cat = df_f.groupby('Category')['Sales'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6, 3.5))
        bars = ax.bar(vendas_cat.index, vendas_cat.values, color=CORES[:len(vendas_cat)], width=0.5, edgecolor='white')
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8000,
                    f'${bar.get_height()/1000:.0f}k', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#374151')
        ax.set_title("Vendas por Categoria", fontsize=13, fontweight='bold', color='#111827', pad=12)
        ax.set_ylabel("Vendas (USD)", fontsize=10, color='#6B7280')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1000:.0f}k'))
        ax.tick_params(colors='#6B7280')
        fig.patch.set_facecolor('white')
        plt.tight_layout()
        st.pyplot(fig)

with c2:
    with st.container():
        lucro_reg = df_f.groupby('Region')['Profit'].sum().sort_values(ascending=False)
        cores_reg = [CORES[0] if v >= 0 else "#EF4444" for v in lucro_reg.values]
        fig, ax = plt.subplots(figsize=(6, 3.5))
        bars = ax.bar(lucro_reg.index, lucro_reg.values, color=cores_reg, width=0.5, edgecolor='white')
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
                    f'${bar.get_height()/1000:.0f}k', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#374151')
        ax.set_title("Lucro por Região", fontsize=13, fontweight='bold', color='#111827', pad=12)
        ax.set_ylabel("Lucro (USD)", fontsize=10, color='#6B7280')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1000:.0f}k'))
        ax.tick_params(colors='#6B7280')
        fig.patch.set_facecolor('white')
        plt.tight_layout()
        st.pyplot(fig)

# ── Linha 2: Evolução mensal ──────────────────────────────────────────
st.markdown('<div class="section-title">Evolução Mensal das Vendas</div>', unsafe_allow_html=True)

vendas_mes = df_f.groupby('Month')['Sales'].sum()
fig, ax = plt.subplots(figsize=(14, 3.8))
ax.fill_between(range(len(vendas_mes)), vendas_mes.values, alpha=0.15, color=CORES[0])
ax.plot(range(len(vendas_mes)), vendas_mes.values, color=CORES[0], linewidth=2.5, marker='o', markersize=4)
ax.set_xticks(range(len(vendas_mes)))
ax.set_xticklabels([str(m) for m in vendas_mes.index], rotation=45, ha='right', fontsize=8, color='#6B7280')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1000:.0f}k'))
ax.tick_params(colors='#6B7280')
ax.set_title("Vendas mensais ao longo do tempo", fontsize=13, fontweight='bold', color='#111827', pad=12)
fig.patch.set_facecolor('white')
plt.tight_layout()
st.pyplot(fig)

# ── Linha 3: Pizza + Top 10 ───────────────────────────────────────────
st.markdown('<div class="section-title">Participação e Top Produtos</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    vendas_cat2 = df_f.groupby('Category')['Sales'].sum()
    fig, ax = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax.pie(
        vendas_cat2.values,
        labels=vendas_cat2.index,
        autopct='%1.1f%%',
        colors=CORES[:len(vendas_cat2)],
        startangle=140,
        wedgeprops=dict(edgecolor='white', linewidth=2)
    )
    for text in autotexts:
        text.set_fontsize(11)
        text.set_fontweight('bold')
    ax.set_title("Participação das Categorias", fontsize=13, fontweight='bold', color='#111827', pad=12)
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    st.pyplot(fig)

with c4:
    top10 = df_f.groupby('Product Name')['Sales'].sum().sort_values(ascending=True).tail(10)
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.barh(top10.index, top10.values, color=CORES[0], edgecolor='white')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1000:.0f}k'))
    ax.tick_params(colors='#6B7280', labelsize=8)
    ax.set_title("Top 10 Produtos por Vendas", fontsize=13, fontweight='bold', color='#111827', pad=12)
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    st.pyplot(fig)

# ── Tabela de dados ───────────────────────────────────────────────────
st.markdown('<div class="section-title">Dados Detalhados</div>', unsafe_allow_html=True)
with st.expander("🔍 Ver tabela de dados"):
    st.dataframe(
        df_f[['Order Date', 'Category', 'Sub-Category', 'Product Name', 'Region', 'Sales', 'Profit']]
        .sort_values('Sales', ascending=False)
        .reset_index(drop=True),
        use_container_width=True
    )