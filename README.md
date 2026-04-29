# 📊 Proyek Analisis Data E-Commerce

Dashboard interaktif dan analisis end-to-end berbasis **Brazilian E-Commerce Public Dataset**,
mencakup data wrangling, assessing data, EDA, RFM analysis, dan visualisasi melalui Streamlit.

---

## 🚀 Cara Menjalankan

### 1. Setup Environment — Anaconda (VSCode)

Buka **Anaconda Prompt** atau terminal terintegrasi di VSCode, lalu jalankan perintah berikut
untuk membuat environment baru khusus proyek ini:

```bash
conda create --name ecommerce-analysis python=3.12
conda activate ecommerce-analysis
```

Pastikan environment yang aktif sudah dipilih sebagai **Python Interpreter** di VSCode:
`Ctrl + Shift + P` → `Python: Select Interpreter` → pilih environment Anaconda yang sesuai.

---

### 2. Setup Environment — Shell/Terminal

Setelah environment aktif, install semua dependensi dari file `requirements.txt`:

```bash
pip install -r requirements.txt
```

> **Catatan:** `main_data.csv` dihasilkan secara otomatis saat menjalankan seluruh cell pada
> `notebook.ipynb`. Jalankan notebook dari awal hingga akhir terlebih dahulu sebelum
> menjalankan dashboard.

---

### 3. Run Streamlit App

Masuk ke folder `dashboard`, lalu jalankan aplikasi:

```bash
cd dashboard
streamlit run dashboard.py

dapat dilakukan juga
https://dashboardpy-hasil.streamlit.app/ (hasil saat ini)
```

## 📁 Deskripsi Dataset

Dataset yang digunakan adalah **Brazilian E-Commerce Public Dataset** dari Olist, terdiri dari
9 file CSV yang saling berelasi dan mencakup periode transaksi **2016–2018**.

| File | Deskripsi |
|---|---|
| `customers_dataset.csv` | Data pelanggan termasuk `customer_id` dan lokasi |
| `orders_dataset.csv` | Header order utama, status, dan waktu pembelian |
| `order_items_dataset.csv` | Detail item per order, harga, dan ongkos kirim |
| `order_payments_dataset.csv` | Informasi pembayaran dan cicilan per order |
| `order_reviews_dataset.csv` | Review dan rating pelanggan per order |
| `products_dataset.csv` | Daftar produk beserta kategori (bahasa Portugis) |
| `sellers_dataset.csv` | Informasi penjual dan lokasi |
| `geolocation_dataset.csv` | Koordinat geografis berdasarkan kode pos |
| `product_category_name_translation.csv` | Terjemahan kategori produk ke bahasa Inggris |

---

## 🔍 Pertanyaan Bisnis

Proyek ini dirancang untuk menjawab tiga pertanyaan bisnis utama:

1. **Bagaimana tren revenue dan jumlah order per bulan selama periode 2017–2018?**
2. **Kategori produk mana yang menghasilkan revenue tertinggi selama periode ini?**
3. **State pelanggan mana yang memberikan kontribusi penjualan terbesar?**

---

## 📊 Hasil Analisis

### Pertanyaan 1 — Tren Revenue & Order Bulanan

Tren revenue dan jumlah order per bulan selama 2017–2018 menunjukkan **pola musiman yang
signifikan**. Terdapat lonjakan volume order dan revenue pada bulan-bulan tertentu, terutama
menjelang akhir tahun dan pertengahan tahun. Puncak revenue terjadi di bulan **November 2017**
yang kemungkinan besar dipengaruhi oleh event promosi besar seperti Black Friday.

Secara keseluruhan, tren revenue menunjukkan **pertumbuhan positif** dari awal 2017 hingga
pertengahan 2018, mencerminkan ekspansi bisnis yang konsisten. Pola ini penting sebagai dasar
perencanaan promosi dan ketersediaan stok pada periode high-demand.

---

### Pertanyaan 2 — Kategori Produk dengan Revenue Tertinggi

Dari seluruh kategori produk yang tersedia, kategori **health_beauty, watches_gifts,
dan bed_bath_table** secara konsisten masuk dalam 10 besar kontributor revenue. Kategori-kategori
ini menjadi prioritas utama dalam alokasi anggaran pemasaran dan manajemen inventori karena
menghasilkan pendapatan tertinggi secara absolut.

Kategori dengan volume order tinggi namun revenue rendah mengindikasikan produk bernilai kecil
yang terjual massal — strategi bundling dapat diterapkan untuk meningkatkan nilai transaksinya.

---

### Pertanyaan 3 — State dengan Kontribusi Penjualan Terbesar

State **SP (São Paulo)** mendominasi penjualan secara signifikan dibandingkan state lainnya,
diikuti oleh **RJ (Rio de Janeiro)** dan **MG (Minas Gerais)**. Ketiga state ini berada di
wilayah tenggara Brasil yang merupakan pusat ekonomi utama negara tersebut.

Konsentrasi penjualan yang tinggi di SP menunjukkan peluang sekaligus risiko ketergantungan
pada satu wilayah. Diversifikasi pasar ke state-state dengan potensi pertumbuhan seperti
**PR, RS, dan BA** dapat menjadi strategi ekspansi yang layak dipertimbangkan.

---

### Analisis Lanjutan — RFM Segmentation

Analisis RFM (Recency, Frequency, Monetary) dilakukan untuk mengklasifikasikan pelanggan ke
dalam tiga segmen berdasarkan nilai transaksi mereka:

| Segmen | Karakteristik | Strategi |
|---|---|---|
| **High Value** | Pembelian besar, sering, dan baru-baru ini | Program loyalitas eksklusif & early access |
| **Mid Value** | Pembelian moderat dan cukup rutin | Upselling, bundling, rekomendasi produk premium |
| **Low Value** | Pembelian kecil atau jarang | Retargeting ads, diskon first-repeat-purchase |

Distribusi segmen menunjukkan mayoritas pelanggan berada pada segmen **Low Value**, yang
mengindikasikan banyaknya pelanggan yang hanya melakukan pembelian satu kali. Hal ini
menegaskan pentingnya strategi retensi pelanggan untuk meningkatkan Lifetime Value (LTV).

Boxplot pada skala logaritmik memperlihatkan bahwa segmen **High Value** memiliki penyebaran
data yang sangat lebar dengan banyak outlier ekstrem — sejalan dengan **Prinsip Pareto (80/20)**
di mana sebagian kecil pelanggan menyumbang sebagian besar total revenue.

