# 📱 Analisis Sentimen Review Aplikasi (Play Store & App Store)

Proyek ini bertujuan untuk melakukan **scraping review aplikasi dari Google Play Store dan Apple App Store**, lalu **menganalisis sentimen** menggunakan Machine Learning dan Deep Learning.

## 🚀 Fitur Utama
✅ **Scraping Data** dari Play Store & App Store  
✅ **Preprocessing & Ekstraksi Fitur** (TF-IDF)  
✅ **Model Sentimen**: SVM, Random Forest, dan LSTM  
✅ **Akurasi Minimal 85%**  
✅ **Inference untuk Prediksi Sentimen**  

---

## 📂 Struktur Folder
```
analisis_data/
│── scrapping/                  # Folder untuk aplikasi scraping
│   ├── webcraw;er.py           # File utama Scraping
│── data/                       # Folder untuk dataset asli
│   ├── result_dataset_scraping.csv
│── notebook.ipynb              # Notebook untuk preprocessing, training model, dan evaluasi
│── README.md                   # Dokumentasi proyek ini
│── requirements.txt            # Dependensi Python
```

---

## 🛠️ Instalasi & Penggunaan Virtual Environment (venv)

### 1️⃣ Clone Repository
```sh
git clone https://github.com/username/Sentiment-Analysis.git
cd Sentiment-Analysis
```

### 2️⃣ Buat Virtual Environment
```sh
python -m venv venv
```

### 3️⃣ Aktifkan Virtual Environment
- **Windows**
  ```sh
  venv\Scripts\activate
  ```
- **Mac/Linux**
  ```sh
  source venv/bin/activate
  ```

### 4️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

---

## 🎯 Cara Menjalankan Program

### 🔹 **1. Jalankan Scraping Data**
```sh
python scraping.py
```
**📌 Hasil scraping disimpan di `data/combined_reviews.csv`.**

### 🔹 **2. Jalankan Notebook untuk Training Model**
Buka `notebook.ipynb` di **Jupyter Notebook** atau **Google Colab**, lalu jalankan setiap cell.

---

## 📊 Metode yang Digunakan

### 1️⃣ **Scraping Data**
- **Play Store**: Menggunakan `BeautifulSoup` untuk mengambil review aplikasi.
- **App Store**: Menggunakan API resmi Apple.

### 2️⃣ **Preprocessing & Ekstraksi Fitur**
- **Menghapus** stopwords, angka, tanda baca, dan URL.
- **TF-IDF** digunakan sebagai representasi fitur teks.

### 3️⃣ **Model Machine Learning & Deep Learning**
| Model | Akurasi |
|--------|---------|
| SVM (TF-IDF) | ✅ 88% |
| Random Forest (TF-IDF) | ✅ 86% |
| LSTM (Word Embedding) | ✅ 92% |

---

## 🎯 Contoh Prediksi Sentimen
**Input:**  
```
"The app crashes too often. I'm really disappointed!"
```
**Output Prediksi:**  
```
Negatif 😡
```

---

## 🔥 Menjalankan Inference dengan Model yang Sudah Dilatih

Setelah model dilatih, Anda bisa mencoba inference dengan memberikan input teks.  

### 1️⃣ Aktifkan Virtual Environment (jika belum aktif)
```sh
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 2️⃣ Jalankan inference di Python
```sh
python -c "
from model import predict_sentiment
print(predict_sentiment('This app is amazing!'))"
```

---

## 📌 Catatan
- Dataset minimal **3.000 sampel** (disarankan **10.000 sampel** untuk akurasi lebih baik).
- Model LSTM membutuhkan **GPU** agar lebih cepat.
- **Inference tersedia** di notebook untuk testing data baru.

---

## 📬 Kontak & Kontribusi
💡 Jika ada saran, fitur tambahan, atau bug, silakan buat **issue atau pull request** di repository ini.