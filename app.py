# app.py
import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go

# Load data dan model
df = pd.read_csv("data_tempat_wisata_clustered.csv")
kmeans = joblib.load("model_kmeans.pkl")

# Page configuration
st.set_page_config(
    page_title="Rekomendasi Wisata Bali", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏝️"
)

# Custom CSS untuk styling yang lebih menarik
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #666;
        margin: 0.5rem 0 0 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Filter section */
    .filter-section {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Data table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        text-align: center;
    }
    
    /* Stats container */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    /* Map container */
    .map-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header dengan animasi gradient
st.markdown("""
<div class="main-header">
    <h1>🏝️ Sistem Rekomendasi Tempat Wisata Bali</h1>
    <p>Temukan destinasi wisata terbaik di Pulau Dewata dengan teknologi AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar dengan styling yang lebih menarik
with st.sidebar:
    st.markdown("### 🔍 **Filter Pencarian**")
    
    # Filter area dengan icon
    st.markdown("*Pilih Lokasi**")
    selected_area = st.selectbox(
        "",
        options=["Semua Wilayah"] + sorted(df["kabupaten_kota"].unique().tolist()),
        key="area_select"
    )
    st.markdown("**Pilih Kategori**")
    selected_category = st.selectbox(
        "",
        options=["Semua Kategori"] + sorted(df["kategori"].unique().tolist()),
        key="category_select"
    )
    
    # Tambahan info di sidebar
    st.markdown("---")
    st.markdown("**Statistik Data**")
    st.info(f"📍 **Total Lokasi**: {len(df)} tempat")
    st.info(f"🗺️ **Wilayah**: {df['kabupaten_kota'].nunique()} kabupaten/kota")
    st.info(f"🎯 **Kategori**: {df['kategori'].nunique()} jenis wisata")

# Filter data
filtered_df = df.copy()
if selected_area != "Semua Wilayah":
    filtered_df = filtered_df[filtered_df["kabupaten_kota"] == selected_area]

if selected_category != "Semua Kategori":
    filtered_df = filtered_df[filtered_df["kategori"] == selected_category]

# Metrics cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(filtered_df)}</div>
        <div class="metric-label">🏖️ Tempat Wisata</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_rating = filtered_df['rating'].mean() if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_rating:.1f}</div>
        <div class="metric-label">⭐ Rating Rata-rata</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    top_category = filtered_df['kategori'].mode().iloc[0] if len(filtered_df) > 0 else "-"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="font-size: 1.5rem;">{top_category}</div>
        <div class="metric-label">🎯 Kategori Terpopuler</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    clusters = filtered_df['cluster'].nunique() if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{clusters}</div>
        <div class="metric-label">🔬 Cluster Aktif</div>
    </div>
    """, unsafe_allow_html=True)

# Visualisasi data dengan charts
if len(filtered_df) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="section-header">📊 Distribusi Kategori</h3>', unsafe_allow_html=True)
        category_counts = filtered_df['kategori'].value_counts()
        fig_pie = px.pie(
            values=category_counts.values, 
            names=category_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="section-header">⭐ Distribusi Rating</h3>', unsafe_allow_html=True)
        fig_hist = px.histogram(
            filtered_df, 
            x='rating', 
            nbins=20,
            color_discrete_sequence=['#FF6B6B']
        )
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_title="Rating",
            yaxis_title="Jumlah Tempat"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

# Tabel data dengan styling
st.markdown('<h2 class="section-header">📋 Daftar Rekomendasi Wisata</h2>', unsafe_allow_html=True)

if len(filtered_df) > 0:
    # Format data untuk tampilan yang lebih menarik
    display_df = filtered_df[["nama", "kategori", "kabupaten_kota", "rating", "preferensi"]].copy()
    display_df.columns = ["🏖️ Nama Tempat", "🎯 Kategori", "📍 Lokasi", "⭐ Rating", "❤️ Preferensi"]
    
    # Styling untuk rating
    display_df["⭐ Rating"] = display_df["⭐ Rating"].apply(lambda x: f"{x:.1f} ⭐")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data CSV",
        data=csv,
        file_name=f"wisata_bali_{selected_area}_{selected_category}.csv",
        mime="text/csv"
    )
else:
    st.warning("🔍 Tidak ada data yang sesuai dengan filter yang dipilih.")

# Peta interaktif dengan styling yang lebih menarik
st.markdown('<h2 class="section-header">🗺️ Peta Interactive Lokasi Wisata</h2>', unsafe_allow_html=True)

if len(filtered_df) > 0:
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    
    # Buat peta dengan tema yang lebih menarik
    m = folium.Map(
        location=[-8.4, 115.2], 
        zoom_start=10,
        tiles='CartoDB Positron'  # Tema yang lebih bersih
    )
    
    # Warna untuk tiap cluster dengan palet yang lebih menarik
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
    
    # Tambahkan marker dengan popup yang lebih informatif
    for _, row in filtered_df.iterrows():
        cluster_id = int(row['cluster'])
        
        # HTML untuk popup yang lebih menarik
        popup_html = f"""
        <div style='width: 200px; font-family: Arial;'>
            <h4 style='color: {colors[cluster_id]}; margin-bottom: 10px;'>{row['nama']}</h4>
            <p><b>📍 Lokasi:</b> {row['kabupaten_kota']}</p>
            <p><b>🎯 Kategori:</b> {row['kategori']}</p>
            <p><b>⭐ Rating:</b> {row['rating']:.1f}/5</p>
            <p><b>❤️ Preferensi:</b> {row['preferensi']}</p>
        </div>
        """
        
        folium.CircleMarker(
            location=(row['latitude'], row['longitude']),
            radius=8,
            color='white',
            weight=2,
            fill=True,
            fillColor=colors[cluster_id],
            fillOpacity=0.8,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(m)
    
    # Tambahkan legend untuk cluster
    legend_html = """
    <div style='position: fixed; 
                bottom: 50px; left: 50px; width: 120px; height: auto; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px; border-radius: 5px; color: black
                '>
    <p style='margin: 0; font-weight: bold;'>Cluster Legend:</p>
    """
    
    for i, color in enumerate(colors[:filtered_df['cluster'].nunique()]):
        legend_html += f"<p style='margin: 5px 0;'><i style='background:{color}; width: 12px; height: 12px; display: inline-block; border-radius: 50%;'></i> Cluster {i}</p>"
    
    legend_html += "</div>"
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Tampilkan peta
    st_data = st_folium(m, width=None, height=500)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer dengan informasi tambahan
# st.markdown("---")
# st.markdown("""
# <div style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 10px; margin-top: 2rem;'>
#     <h4 style='color: white; margin-bottom: 1rem;'>🏝️ Explore Beautiful Bali</h4>
#     <p style='color: rgba(255,255,255,0.8); margin: 0;'>
#         Sistem rekomendasi ini menggunakan teknologi Machine Learning untuk memberikan saran wisata terbaik
#         berdasarkan preferensi dan lokasi pilihan Anda.
#     </p>
# </div>
# """, unsafe_allow_html=True)