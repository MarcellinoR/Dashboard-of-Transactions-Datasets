import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# 1. SETUP & PREMIUM STYLING
st.set_page_config(page_title="Finance Intelligence Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1c24 0%, #11131a 100%);
        padding: 20px; border-radius: 15px;
        border: 1px solid rgba(0, 212, 255, 0.1);
        border-left: 5px solid #00d4ff;
    }
    h1, h2, h3 { color: #ffffff; font-family: 'Segoe UI', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA LOADING
FILE_PATH = r'transactions.csv'

@st.cache_data
def load_data():
    try:
        data = pd.read_csv(FILE_PATH)
        data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y', errors='coerce')
        return data
    except:
        return pd.DataFrame()

df_init = load_data()

# 3. SIDEBAR
st.sidebar.title("💎 Control Center")
if not df_init.empty:
    list_category = df_init['Category'].unique().tolist()
    selected_cat = st.sidebar.multiselect("Select Categories:", list_category, default=list_category)
    df = df_init[df_init['Category'].isin(selected_cat)]
else:
    st.stop()

# 4. HEADER & TOP 4 KPI (Visual 1, 2, 3)
st.title("📊 Executive Financial Overview")
st.markdown("---")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Revenue", f"${df['Amount'].sum():,.0f}")
kpi2.metric("Avg Transaction", f"${df['Amount'].mean():,.1f}")
kpi3.metric("Total Volume", f"{len(df)} Trx")
kpi4.metric("Efficiency Score", f"{(1 - (df['Processing_Time_Seconds'].mean()/5))*100:.1f}%")

# 5. MAIN ROW (Visual 4 & 5)
row1_1, row1_2 = st.columns([2, 1])

with row1_1:
    st.subheader("📈 Financial Growth & Cash Flow")
    df_trend = df.groupby([df['Date'].dt.to_period('M'), 'Transaction_Type'])['Amount'].sum().reset_index()
    df_trend['Date'] = df_trend['Date'].astype(str)
    
    fig_growth = go.Figure()
    for t_type, color in zip(['Debit', 'Credit'], ['#ff4b4b', '#00d4ff']):
        curr = df_trend[df_trend['Transaction_Type'] == t_type]
        fig_growth.add_trace(go.Scatter(
            x=curr['Date'], y=curr['Amount'], name=t_type,
            fill='tozeroy', mode='lines', line=dict(width=3, color=color, shape='spline')
        ))
    fig_growth.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350)
    st.plotly_chart(fig_growth, use_container_width=True)

with row1_2:
    st.subheader("🌓 Transaction Mix")
    fig_mix = px.pie(df, names='Transaction_Type', values='Amount', hole=0.7,
                     color_discrete_sequence=['#ff4b4b', '#00d4ff'])
    fig_mix.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=350)
    st.plotly_chart(fig_mix, use_container_width=True)

# 6. SECOND ROW (Visual 6, 7, 8)
row2_1, row2_2, row2_3 = st.columns(3)

with row2_1:
    st.subheader("🏆 Top Merchants")
    top_m = df.groupby('Merchant_Name')['Amount'].sum().sort_values().tail(5)
    fig_m = px.bar(top_m, orientation='h', template="plotly_dark", color_discrete_sequence=['#00d4ff'])
    fig_m.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, yaxis_title=None)
    st.plotly_chart(fig_m, use_container_width=True)

with row2_2:
    st.subheader("🗺️ Category Treemap")
    fig_tree = px.treemap(df, path=['Category'], values='Amount', color='Amount', color_continuous_scale='Blues')
    fig_tree.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig_tree, use_container_width=True)

with row2_3:
    st.subheader("🎯 Goal Target")
    target = 100000 # Contoh target
    current = df['Amount'].sum()
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = current,
        gauge = {'axis': {'range': [None, target]}, 'bar': {'color': "#00d4ff"}},
        title = {'text': "Revenue vs Target"}
    ))
    fig_gauge.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

# 7. BOTTOM ROW (Visual 9 & 10)
row3_1, row3_2 = st.columns([1, 2])

with row3_1:
    st.subheader("🗓️ Daily Density")
    df['Day'] = df['Date'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heat_df = df.groupby('Day')['Amount'].count().reindex(day_order)
    fig_heat = px.bar(heat_df, color=heat_df.values, color_continuous_scale='GnBu')
    fig_heat.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350, showlegend=False)
    st.plotly_chart(fig_heat, use_container_width=True)

with row3_2:
    st.subheader("📂 Detailed Transaction Records")
    st.dataframe(df.sort_values('Date', ascending=False).head(50), use_container_width=True, height=350)

# --- 8. SMART BUSINESS INSIGHTS (Hal Baru: Auto-Narrative) ---
st.markdown("---")
st.header("💡 Executive Summary & Insights")

# Logika untuk mencari Insight secara otomatis
try:
    # 1. Mencari hari tersibuk
    df['Day'] = df['Date'].dt.day_name()
    busy_day = df['Day'].value_counts().idxmax()
    
    # 2. Mencari kategori pengeluaran terbesar
    top_cat = df.groupby('Category')['Amount'].sum().idxmax()
    
    # 3. Mencari perbandingan Debit vs Credit
    total_debit = df[df['Transaction_Type'] == 'Debit']['Amount'].sum()
    total_credit = df[df['Transaction_Type'] == 'Credit']['Amount'].sum()
    ratio = "sehat" if total_credit > total_debit else "perlu diawasi"

    # Menampilkan Insight dalam kotak info yang rapi
    st.info(f"""
    **Hasil Analisis Otomatis:**
    * **Tren Operasional:** Transaksi paling sering terjadi pada hari **{busy_day}**. Disarankan untuk memastikan sistem pembayaran dalam kondisi prima di hari tersebut.
    * **Fokus Pengeluaran:** Kategori **{top_cat}** merupakan kontributor volume terbesar. Perlu dilakukan evaluasi efisiensi pada kategori ini.
    * **Kesehatan Arus Kas:** Saat ini kondisi arus kas Anda **{ratio}**. Total Credit (Pemasukan) tercatat sebesar ${total_credit:,.2f} dibandingkan Debit sebesar ${total_debit:,.2f}.
    * **Rekomendasi:** Lakukan pembersihan cache sistem dan maintenance rutin pada hari dengan volume terendah untuk menghindari gangguan layanan.
    """)
    
except Exception as e:
    st.write("Insight belum tersedia karena data tidak lengkap.")
