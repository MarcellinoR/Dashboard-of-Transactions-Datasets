# 💎 Finance Intelligence Pro: Executive Transaction Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-ff4b4b.svg)
![Plotly](https://img.shields.io/badge/Visual-Plotly-blueviolet.svg)

## 📌 Deskripsi Proyek
Dashboard ini adalah sistem analisis finansial tingkat eksekutif yang dirancang untuk memantau arus kas (*Cash Flow*), performa merchant, dan efisiensi operasional transaksi. Proyek ini berfokus pada visualisasi data yang bersih (Premium Styling) dan penyediaan insight otomatis berbasis data.

## 🚀 Fitur Utama & Analisis
* **Executive KPI Cards**: Pemantauan real-time untuk Total Revenue, Avg Transaction, dan **Efficiency Score** (berdasarkan waktu pemrosesan).
* **Financial Growth & Cash Flow**: Visualisasi area chart interaktif untuk membandingkan tren *Debit* vs *Credit*.
* **Smart Business Insights**: Fitur narasi otomatis yang mendeteksi hari tersibuk, kategori pengeluaran terbesar, dan rasio kesehatan arus kas secara dinamis.
* **Category Treemap & Goal Tracking**: Memudahkan manajemen untuk melihat alokasi dana terbesar dan progres pencapaian target tahunan.
* **Daily Density Analysis**: Analisis statistik untuk menentukan frekuensi transaksi harian guna optimasi operasional.

## 🛠️ Stack Teknologi
* **Language:** Python 3.x
* **Interface:** Streamlit (Custom CSS Dark Mode)
* **Data Engine:** Pandas & NumPy
* **Graphics:** Plotly Express & Graph Objects (Go)

## 📂 Persyaratan Data
Program ini membaca file `transactions.csv` dengan kolom minimal:
`Date`, `Category`, `Amount`, `Transaction_Type`, `Merchant_Name`, dan `Processing_Time_Seconds`.

## ⚙️ Cara Menjalankan
1. Clone repository ini.
2. Pastikan Anda memiliki file `transactions.csv` di direktori yang sesuai.
3. Install dependensi:
   ```bash
   pip install streamlit pandas plotly numpy
Jalankan aplikasi:

Bash
streamlit run transactions.py
Developed as part of a Data Science & Statistics Portfolio.


---
