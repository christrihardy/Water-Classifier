# **How to Use**

## Requirements
- Python
- Postman (jika ingin prediksi via API/backend)
- Docker 

## **1. Running the program locally**

Untuk menjalankan program, pertama Clone repository [Water Classifier](https://github.com/christrihardy/Water-Classifier) dari Github

Lalu, buka terminal, masuk ke direktori **'Water-Classifier'** dan jalankan command dibawah ini:

- uvicorn src.water-backend:app --reload
- streamlit run water-frontend.py

Done! Anda bisa memilih untuk prediksi via API atau Streamlit. 

**Note:**

- **Ctrl + C** untuk mematikan service.

### Running via Docker
Dengan Docker, tidak perlu mengetik command setiap kali ingin mengaktifkan program. 

Masuk ke direktori **'Water-Classifier'** dan jalankan command dibawah ini via terminal:

- sudo docker compose build
- sudo docker compose up -d

Done! Anda bisa memilih untuk prediksi via API atau Streamlit. "**sudo docker compose down**" untuk mematikan service.

**Note:** 

- Docker Desktop harus berjalan di background/dijalankan dulu sebelum menjalankan command diatas
- **sudo docker compose down** untuk mematikan service.


## **2. Prediction via API Service**

Jika ingin melakukan prediksi dengan API, buka url **(nama_host):8000** di aplikasi **Postman** 

Contoh: buka API di local, gunakan localhost:8000 

![Screenshot](img/api_format.png)

- Pilih 'Body' dan masukkan teks format variabel prediktor persis seperti di gambar untuk melakukan predict
- Nilai angka prediktor bisa anda ubah 
- Klik **'SEND'**
- Hasil prediksi akan keluar, **Potable** atau **Non-Potable**

## **3. Prediction via Streamlit**

Jika anda ingin tampilan sistem yang lebih *user-friendly*, buka url **(nama_host):8501** di web browser anda
![Screenshot](img/streamlit.png)

- Masukkan nilai prediktor di kolom yang tertera
- Klik tombol **Predict**

![Screenshot](img/prediction.png)

- Hasil prediksi akan keluar, apakah air tersebut **Potable** atau **Non-potable**

## **4. Access the online service**

Jika ingin mengakses prediction service dari penulis, buka link ini: **13.213.57.173:8501**

## **5. Retraining Model**

Untuk retraining model, jalankan ke-3 file Python ini sesuai urutan di folder src:

1. data_pipeline.py
2. preprocessing.py
3. modelling. py

Output dari proses ini adalah file pickle production_model.pkl yang akan digunakan oleh backend API untuk prediksi.