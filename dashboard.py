import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Membuat dashboard Streamlit
st.set_page_config(page_title="Analisis Penyewaan Sepeda", layout="wide")

# Title
st.title("Dashboard Analisis Penyewaan Sepeda 🚴‍♂️")

# Sidebar
st.sidebar.header("Menu")
menu = st.sidebar.radio(
    "Pilih Visualisasi:",
    ["Faktor yang Mempengaruhi Penyewaan", "Pola Penggunaan Berdasarkan Jam", "Clustering: Manual Grouping"],
)

# Data Loading
@st.cache_data
def load_data():
    data_hour = pd.read_csv("hour.csv")
    data_day = pd.read_csv("day.csv")
    return data_hour, data_day

data_hour, data_day = load_data()

if menu == "Faktor yang Mempengaruhi Penyewaan":
    st.header("Faktor yang Mempengaruhi Penyewaan Sepeda")
    
    # Heatmap Korelasi
    st.subheader("Heatmap Korelasi")
    plt.figure(figsize=(10, 8))
    sns.heatmap(data_day.corr(), annot=True, fmt=".2f", cmap='coolwarm', linewidths=1, linecolor='white', square=True)
    plt.title("Heatmap Korelasi Fitur - Faktor yang Mempengaruhi Jumlah Penyewaan")
    st.pyplot(plt)
    plt.clf()
    st.markdown("""
    **Insight:**
    - Korelasi yang tinggi ditemukan antara suhu (temp) dan jumlah penyewaan sepeda (cnt). 
    - Kelembaban (hum) memiliki korelasi negatif sedang, yang berarti kelembaban yang lebih tinggi cenderung mengurangi penyewaan sepeda.
    - Kecepatan angin (windspeed) menunjukkan korelasi rendah terhadap jumlah penyewaan.
    """)

    # Boxplot Kondisi Cuaca
    st.subheader("Pengaruh Kondisi Cuaca terhadap Jumlah Penyewaan")
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=data_day, x='weathersit', y='cnt', palette='Set2')
    plt.title("Pengaruh Kondisi Cuaca terhadap Jumlah Penyewaan")
    plt.xlabel("Kondisi Cuaca (1 = Cerah, 2 = Mendung, 3 = Hujan)")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(plt)
    plt.clf()
    st.markdown("""
    **Insight:**
    - Kondisi cuaca yang cerah (kode 1) memiliki jumlah penyewaan sepeda tertinggi, sementara cuaca mendung (kode 2) dan hujan (kode 3) cenderung menurunkan jumlah penyewaan.
    """)
    
    # Scatter Plot
    st.subheader("Pengaruh Suhu, Kelembaban, dan Kecepatan Angin")
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    sns.scatterplot(data=data_day, x='temp', y='cnt', ax=axs[0], color='dodgerblue')
    axs[0].set_title("Pengaruh Suhu terhadap Jumlah Penyewaan")
    axs[0].set_xlabel("Suhu")
    axs[0].set_ylabel("Jumlah Penyewaan")

    sns.scatterplot(data=data_day, x='hum', y='cnt', ax=axs[1], color='darkorange')
    axs[1].set_title("Pengaruh Kelembaban terhadap Jumlah Penyewaan")
    axs[1].set_xlabel("Kelembaban")

    sns.scatterplot(data=data_day, x='windspeed', y='cnt', ax=axs[2], color='seagreen')
    axs[2].set_title("Pengaruh Kecepatan Angin terhadap Jumlah Penyewaan")
    axs[2].set_xlabel("Kecepatan Angin")

    st.pyplot(fig)
    plt.clf()
    st.markdown("""
    **Insight:**
    - Suhu memiliki hubungan positif kuat terhadap jumlah penyewaan sepeda. Penyewaan meningkat saat suhu naik.
    - Kelembaban tinggi menyebabkan penurunan jumlah penyewaan.
    - Kecepatan angin tidak menunjukkan hubungan signifikan dengan jumlah penyewaan sepeda.
    """)
    
elif menu == "Pola Penggunaan Berdasarkan Jam":
    st.header("Pola Penggunaan Berdasarkan Jam dan Kondisi Cuaca")
    # Line Plot Tren Per Jam
    st.subheader("Tren Penyewaan Sepeda Berdasarkan Jam dan Hari")
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=data_hour, x='hr', y='cnt', hue='weekday', palette='viridis')
    plt.title("Pola Penggunaan Sepeda Berdasarkan Jam dan Hari")
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(plt)
    plt.clf()
    st.markdown("""
    **Insight:**
    - Puncak penyewaan sepeda terjadi pada pagi hari (07:00 - 09:00) dan sore hari (17:00 - 19:00), terutama pada hari kerja.
    - Pada akhir pekan, pola penyewaan lebih stabil sepanjang hari tanpa puncak yang jelas.
    """)

    # Boxplot Kondisi Cuaca per Jam
    st.subheader("Boxplot Penyewaan Berdasarkan Kondisi Cuaca per Jam")
    plt.figure(figsize=(14, 6))
    sns.boxplot(data=data_hour, x='hr', y='cnt', hue='weathersit', palette='Set1', linewidth=1.2)
    plt.title("Jumlah Penyewaan Berdasarkan Kondisi Cuaca per Jam")
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(plt)
    st.markdown("""
    **Insight:**
    - Pada cuaca cerah (kode 1), jumlah penyewaan lebih tinggi pada jam sibuk.
    - Cuaca mendung atau hujan menyebabkan penurunan jumlah penyewaan di semua jam.
    """)

    # Barplot Hari Kerja vs Akhir Pekan
    st.subheader("Jumlah Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=data_day, x='workingday', y='cnt', palette='muted')
    plt.title("Jumlah Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan")
    plt.xlabel("Hari Kerja (0 = Akhir Pekan, 1 = Hari Kerja)")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(plt)
    st.markdown("""
    **Insight:**
    - Jumlah penyewaan pada hari kerja lebih tinggi dibandingkan akhir pekan.
    - Ini menunjukkan bahwa sepeda lebih sering digunakan untuk keperluan kerja atau transportasi rutin.
    """)

elif menu == "Clustering: Manual Grouping":
    st.header("Clustering: Manual Grouping")
    # Menambahkan kolom 'Category'
    def categorize_rentals(count):
        if count < 2000:
            return "Rendah"
        elif 2000 <= count <= 4000:
            return "Sedang"
        else:
            return "Tinggi"

    data_day['Category'] = data_day['cnt'].apply(categorize_rentals)

    # Menghitung distribusi kategori
    category_counts = data_day['Category'].value_counts()

    # Visualisasi distribusi kategori
    st.subheader("Distribusi Kategori Penyewaan Sepeda")
    plt.figure(figsize=(8, 6))
    sns.barplot(x=category_counts.index, y=category_counts.values, palette="viridis")
    plt.title("Distribusi Kategori Penyewaan Sepeda", fontsize=14)
    plt.xlabel("Kategori Penyewaan", fontsize=12)
    plt.ylabel("Jumlah Hari", fontsize=12)
    st.pyplot(plt)
    plt.clf()
    st.markdown("""
    **Hasil Visualisasi:**
    - Grafik batang menampilkan jumlah hari untuk setiap kategori (Rendah, Sedang, Tinggi).
    - Anda dapat langsung mengidentifikasi pola perilaku harian berdasarkan jumlah penyewaan.

    **Analisis:**
    - Jika jumlah hari dalam kategori "Rendah" mendominasi, berarti penyewaan sepeda secara umum kurang maksimal.
    - Sebaliknya, jika kategori "Tinggi" mendominasi, bisa dikatakan bahwa penyewaan sepeda sangat populer.
    """)
