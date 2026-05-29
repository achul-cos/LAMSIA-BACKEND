1. Clone proyek github ini ke perangkat komputer anda

2. Pada file .env.example, silahkan duplicate dan ganti namanya menjadi .env

3. Nyalakan server mysql anda (bisa secara local), dan buat database baru (disarankan nama database yang baru itu yaitu lamsia_db)

4. Pada file .env, tambahkan mysql host, mysql port, mysql user(disarankan root), mysql user password, dan nama database baru yang anda berikan

5. Jalankan virtual envrioment python, dengan buka powershell dan ganti path powershell nya menjadi path proyek ini, lalu jalankan perintan CLI

python -m venv venv

6. Install beberapa package dengan menjalankan perintah CLI

pip install fastapi uvicorn sqlalchemy pymysql python-dotenv

7. Lalu jalankan server FastAPI

uvicorn app.main:app --reload

8. Server dianggap berjalan jika kamu dapat mengakses link server yang keluar di terminal, contohnya:

http://127.0.0.1:8000

