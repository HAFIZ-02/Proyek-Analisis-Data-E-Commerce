"""
E-Commerce Data Analysis Dashboard
Berdasarkan dataset E-Commerce Public Dataset
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# =========================
# 1. SETUP
# =========================

st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .block-container { padding-top: 1.5rem; }
    .metric-container {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }
    h1 { color: #1a1a2e; }
    h2, h3 { color: #16213e; }
    .stMetric label { font-size: 0.85rem !important; color: #666 !important; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; }
    .insight-box {
        background: #e8f4fd;
        border-left: 4px solid #2196F3;
        padding: 10px 15px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .rec-box {
        background: #e8f5e9;
        border-left: 4px solid #4CAF50;
        padding: 10px 15px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 2. LOAD DATA
# =========================

@st.cache_data
def load_data():
    import os
    BASE_DIR = os.path.dirname(Proyek-Analisis-Data-E-Commerce/dashboard/dashboard.py)
    csv_path = os.path.join(BASE_DIR, 'main_data.csv')
    df = pd.read_csv(csv_path)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
    df['order_year'] = df['order_purchase_timestamp'].dt.year
    df['order_month_num'] = df['order_purchase_timestamp'].dt.month
    df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

    # Pastikan kolom yang dibutuhkan ada
    if 'primary_category' not in df.columns and 'product_category_name' in df.columns:
        df['primary_category'] = df['product_category_name']
    if 'revenue' not in df.columns and 'total_payment' in df.columns:
        df['revenue'] = df['total_payment']

    return df

try:
    df = load_data()
    df = df[df['primary_category'] != 'Unknown']
    data_loaded = True
except FileNotFoundError:
    st.error("⚠️ File `main_data.csv` tidak ditemukan. Pastikan file berada di direktori yang sama dengan `app.py`.")
    st.info("Letakkan `main_data.csv` di folder `dashboard/` bersama `app.py`, lalu jalankan ulang.")
    st.stop()

# =========================
# 3. HEADER
# =========================

st.title("📊 E-Commerce Data Analysis Dashboard")
st.markdown(
    "Dashboard interaktif untuk analisis **performa penjualan**, **kategori produk**, "
    "**wilayah pelanggan**, dan **segmentasi RFM** — periode **2017–2018**."
)
st.markdown("---")

# =========================
# 4. SIDEBAR FILTER
# =========================

st.sidebar.title("🔎 Filter Data")

year_options = sorted(df['order_year'].dropna().unique().tolist())
year_filter = st.sidebar.multiselect(
    "Pilih Tahun",
    options=year_options,
    default=year_options,
    help="Filter berdasarkan tahun pembelian"
)

state_options = sorted(df['customer_state'].dropna().unique().tolist())
state_filter = st.sidebar.multiselect(
    "Pilih State",
    options=state_options,
    default=state_options,
    help="Filter berdasarkan state pelanggan"
)

category_options = sorted(df['primary_category'].dropna().unique().tolist())
category_filter = st.sidebar.multiselect(
    "Pilih Kategori",
    options=category_options,
    default=category_options,
    help="Filter berdasarkan kategori produk"
)

# Apply filter
df_filtered = df[
    (df['order_year'].isin(year_filter)) &
    (df['customer_state'].isin(state_filter)) &
    (df['primary_category'].isin(category_filter))
]
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Data:** {len(df_filtered):,} baris")

# =========================
# 5. KPI METRICS
# =========================

col1, col2, col3, col4 = st.columns(4)

total_revenue = df_filtered['revenue'].sum() if 'revenue' in df_filtered.columns else df_filtered['total_payment'].sum()
total_orders = df_filtered['order_id'].nunique()
total_customers = df_filtered['customer_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

with col1:
    st.metric("💰 Total Revenue", f"R$ {total_revenue:,.0f}")
with col2:
    st.metric("📦 Total Orders", f"{total_orders:,}")
with col3:
    st.metric("👤 Total Customers", f"{total_customers:,}")
with col4:
    st.metric("🧾 Avg Order Value", f"R$ {avg_order_value:,.0f}")

st.markdown("---")

# =========================
# 6. VISUALISASI - ROW 1
# =========================

col_left, col_right = st.columns([3, 2])

# Revenue Trend
with col_left:
    st.subheader("📈 Tren Revenue Bulanan")

    rev_col = 'revenue' if 'revenue' in df_filtered.columns else 'total_payment'
    monthly_rev = (
        df_filtered.groupby('order_month')[rev_col]
        .sum()
        .reset_index()
        .sort_values('order_month')
    )

    fig, ax = plt.subplots(figsize=(9, 4))
    x_idx = range(len(monthly_rev))
    ax.plot(
        x_idx,
        monthly_rev[rev_col],
        color='#2196F3', linewidth=2.5, marker='o', markersize=4
        )
    ax.fill_between(x_idx, monthly_rev[rev_col], alpha=0.12, color='#2196F3')
    ax.set_xticks(list(x_idx))
    ax.set_xticklabels(monthly_rev['order_month'], rotation=45, ha='right', fontsize=8)
    ax.fill_between(range(len(monthly_rev)), monthly_rev[rev_col], alpha=0.12, color='#2196F3')
    ax.set_title("Revenue per Bulan", fontsize=13, fontweight='bold', pad=10)
    ax.set_xlabel("Bulan", fontsize=10)
    ax.set_ylabel("Revenue (R$)", fontsize=10)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    sns.despine()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Order Count Trend
with col_right:
    st.subheader("📦 Jumlah Order Bulanan")

    monthly_orders = (
        df_filtered.groupby('order_month')['order_id']
        .nunique()
        .reset_index()
        .sort_values('order_month')
    )

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.bar(
        monthly_orders['order_month'],
        monthly_orders['order_id'],
        color='#7C4DFF', alpha=0.8
    )
    ax2.set_title("Order per Bulan", fontsize=13, fontweight='bold', pad=10)
    ax2.set_xlabel("Bulan", fontsize=10)
    ax2.set_ylabel("Jumlah Order", fontsize=10)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    ax2.grid(axis='y', linestyle='--', alpha=0.4)
    sns.despine()
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

st.markdown("---")

# =========================
# 7. VISUALISASI - ROW 2
# =========================

col_a, col_b = st.columns(2)

# Top Category
with col_a:
    st.subheader("🏆 Top 10 Kategori by Revenue")

    rev_col = 'revenue' if 'revenue' in df_filtered.columns else 'total_payment'
    top_cat = (
        df_filtered.groupby('primary_category')[rev_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig3, ax3 = plt.subplots(figsize=(7, 5))
    colors = sns.color_palette("Blues_r", len(top_cat))
    bars = ax3.barh(top_cat.index[::-1], top_cat.values[::-1], color=colors[::-1])
    ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}K'))
    ax3.set_xlabel("Revenue (R$)", fontsize=10)
    ax3.set_title("Kategori Terbaik", fontsize=13, fontweight='bold', pad=10)
    ax3.grid(axis='x', linestyle='--', alpha=0.4)
    sns.despine()
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close()

# Top State
with col_b:
    st.subheader("🌍 Top 10 State by Revenue")

    top_state = (
        df_filtered.groupby('customer_state')[rev_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig4, ax4 = plt.subplots(figsize=(7, 5))
    colors2 = sns.color_palette("Greens_r", len(top_state))
    ax4.barh(top_state.index[::-1], top_state.values[::-1], color=colors2[::-1])
    ax4.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}K'))
    ax4.set_xlabel("Revenue (R$)", fontsize=10)
    ax4.set_title("State Terbaik", fontsize=13, fontweight='bold', pad=10)
    ax4.grid(axis='x', linestyle='--', alpha=0.4)
    sns.despine()
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close()

st.markdown("---")

# =========================
# 8. RFM ANALYSIS
# =========================

st.subheader("🧠 RFM Analysis — Segmentasi Pelanggan")

if df_filtered.empty:
    st.warning("Tidak ada data untuk filter yang dipilih. Silakan ubah filter di sidebar.")
    st.stop()

snapshot_date = df_filtered['order_purchase_timestamp'].max()

rfm = df_filtered.groupby('customer_id').agg(
    Recency=('order_purchase_timestamp', lambda x: (snapshot_date - x.max()).days),
    Frequency=('order_id', 'nunique'),
    Monetary=(rev_col, 'sum')
).reset_index()

rfm['Segment'] = pd.cut(
    rfm['Monetary'],
    bins=3,
    labels=['Low Value', 'Mid Value', 'High Value']
)

col_rfm1, col_rfm2, col_rfm3 = st.columns(3)

segment_count = rfm['Segment'].value_counts()

with col_rfm1:
    fig5, ax5 = plt.subplots(figsize=(5, 4))
    colors_rfm = ['#FF7043', '#FFC107', '#4CAF50']
    ax5.bar(segment_count.index, segment_count.values, color=colors_rfm)
    ax5.set_title("Distribusi Segmen Pelanggan", fontsize=12, fontweight='bold')
    ax5.set_ylabel("Jumlah Pelanggan")
    ax5.grid(axis='y', linestyle='--', alpha=0.4)
    sns.despine()
    plt.tight_layout()
    st.pyplot(fig5)
    plt.close()

with col_rfm2:
    fig6, ax6 = plt.subplots(figsize=(5, 4))
    ax6.scatter(rfm['Recency'], rfm['Monetary'], alpha=0.3, color='#2196F3', s=15)
    ax6.set_xlabel("Recency (days)")
    ax6.set_ylabel("Monetary (R$)")
    ax6.set_title("Recency vs Monetary", fontsize=12, fontweight='bold')
    ax6.grid(linestyle='--', alpha=0.3)
    sns.despine()
    plt.tight_layout()
    st.pyplot(fig6)
    plt.close()

with col_rfm3:
    st.markdown("**📋 RFM Summary**")
    rfm_summary = rfm[['Recency', 'Frequency', 'Monetary']].describe().round(1)
    st.dataframe(rfm_summary, use_container_width=True)

st.markdown("---")

# =========================
# 9. AUTO INSIGHT
# =========================

st.subheader("📌 Auto Insights")

# Revenue trend
if len(monthly_rev) >= 2:
    trend = "📈 meningkat" if monthly_rev[rev_col].iloc[-1] > monthly_rev[rev_col].iloc[0] else "📉 menurun"
else:
    trend = "stabil"

top_category = top_cat.index[0]
top_cat_value = top_cat.iloc[0]
best_state = top_state.index[0]
dominant_segment = rfm['Segment'].value_counts().idxmax()

c1, c2 = st.columns(2)

with c1:
    st.markdown(f"""
    <div class="insight-box">
    📈 <b>Tren Revenue</b><br>
    Revenue menunjukkan tren <b>{trend}</b> selama periode analisis.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box">
    🏆 <b>Kategori Terbaik</b><br>
    Kategori <b>{top_category}</b> menghasilkan revenue tertinggi sebesar <b>R$ {top_cat_value:,.0f}</b>.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="insight-box">
    🌍 <b>Wilayah Terbaik</b><br>
    State <b>{best_state}</b> merupakan kontributor penjualan terbesar.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box">
    🧠 <b>Segmentasi Customer</b><br>
    Mayoritas pelanggan berada pada segmen <b>{dominant_segment}</b>.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# 10. RECOMMENDATIONS
# =========================

st.subheader("🚀 Rekomendasi Strategis")

if str(dominant_segment) == "Low Value":
    rec = "🎯 Fokus pada promosi agresif dan retargeting ads untuk mendorong pembelian ulang. Pertimbangkan program loyalty poin dan diskon first-repeat-purchase."
elif str(dominant_segment) == "Mid Value":
    rec = "📦 Terapkan strategi upselling dan bundling produk. Kirimkan rekomendasi produk premium berdasarkan riwayat pembelian untuk meningkatkan nilai transaksi."
else:
    rec = "💎 Pertahankan pelanggan high value dengan program eksklusif: early access produk baru, customer service prioritas, dan reward khusus member VIP."

st.markdown(f"""
<div class="rec-box">
{rec}
</div>
""", unsafe_allow_html=True)

# Rekomendasi kategori
st.markdown(f"""
<div class="rec-box" style="margin-top:10px; background:#fff3e0; border-color:#FF9800;">
📦 <b>Fokus Inventori:</b> Tingkatkan stok dan promosi pada kategori <b>{top_category}</b> 
yang secara konsisten menjadi kontributor revenue terbesar.
</div>
""", unsafe_allow_html=True)

# Rekomendasi wilayah
st.markdown(f"""
<div class="rec-box" style="margin-top:10px; background:#fce4ec; border-color:#E91E63;">
🌍 <b>Ekspansi Wilayah:</b> Perkuat penetrasi pasar di luar <b>{best_state}</b> 
dengan membuka logistik baru dan kampanye marketing regional.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# 11. DATA TABLE & DOWNLOAD
# =========================

with st.expander("🔍 Lihat Data Terfilter"):
    st.dataframe(df_filtered.head(200), use_container_width=True)

csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Data Terfilter (CSV)",
    data=csv,
    file_name="filtered_ecommerce_data.csv",
    mime="text/csv"
)

# =========================
# 12. FOOTER
# =========================

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#888; font-size:0.85rem;'>"
    "📊 E-Commerce Dashboard · Dibuat oleh Data Analyst 🚀 · "
    "Dataset: Brazilian E-Commerce Public Dataset"
    "</div>",
    unsafe_allow_html=True
)
