**<div align=center>Initialize Project Into API</div>**

1. Clone proyek github ini ke perangkat komputer anda

2. Pada file .env.example, silahkan duplicate dan ganti namanya menjadi .env

3. Nyalakan server mysql anda (bisa secara local), dan buat database baru (disarankan nama database yang baru itu yaitu lamsia_db), untuk menambahkan database baru bisa menjalan perintah CLI sebagai berikut:

    PS C:\WINDOWS\System32> mysql -u root -p

    // Atau alternatifnya,

    PS C:\Program Files\MySQL\MySQL Server 8.0\bin> mysql -u root -p

    // Setelahnya, masukkan password dari akun root (atau anda dapat ganti dengan akun admin lainya)
    // Setelahnya, anda dapat tambahkan database untuk proyek, sebagai contoh kita akan tambahkan lamsia_db

    mysql> CREATE DATABASE lamsia_db;

    // Setelahnya, untuk memastikan apakah database lamsia_db yang anda tambahkan itu berhasil anda dapat melihat list dari database pada mysql anda, dengan cara,

    mysql> SHOW databases;

    // Jika berhasil, pada output dari perintah mysql tersebut akan muncul database lamsia_db,

    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | lamsia_db          |
    | mysql              |
    | performance_schema |
    | sys                |
    +--------------------+

4. Pada file .env, tambahkan mysql host, mysql port, mysql user(disarankan root), mysql user password, dan nama database baru yang anda berikan, sebagai contoh sebagai berikut untuk pengujian lokal,

    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD=root
    DB_NAME=lamsia_db

5. Jalankan virtual envrioment python, dengan buka powershell dan ganti path powershell nya menjadi path proyek ini, lalu jalankan perintah CLI

    python -m venv venv

5a. Silahkan aktivasi venv nya dengan menjalankan perintah CLI,

    .\venv\Scripts\Activate.ps1

5b. Jika terjadi error seperti berikut, maka jalankan perintah CLI pada poin 5c

    .\venv\Scripts\Activate.ps1 : File C:\LAMSIA\LAMSIA-BACKEND\venv\Scripts\Activate.ps1 cannot be loaded because 
    running scripts is disabled on this system. For more information, see about_Execution_Policies at 
    https:/go.microsoft.com/fwlink/?LinkID=135170.
    At line:1 char:1
    + .\venv\Scripts\Activate.ps1
    + ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        + CategoryInfo          : SecurityError: (:) [], PSSecurityException
        + FullyQualifiedErrorId : UnauthorizedAccess

5c. Jalankan perintah CLI berikut jika terjadi error seperti di poin 5b,

    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

5d. Jika perintah CLI pada poin 5c tidak dapat dijalankan, maka ada kemungkinan anda tidak memiliki hak administrator. Maka jalankan perintah CLI berikut sebagai alternatif,

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

5e. Alternatif paling akhir yaitu menggunakan venv dengan cara seperti ini,

    .\venv\Scripts\python.exe              \\ Ini bentuk dasar dari perintah CLInya 

    .\venv\Scripts\python.exe --version

    .\venv\Scripts\python.exe -m pip list

    .\venv\Scripts\python.exe -m uvicorn app.main:app --reload

6. Install beberapa package dengan menjalankan perintah CLI

    pip install fastapi uvicorn sqlalchemy pymysql python-dotenv

7. Lalu jalankan server FastAPI

    uvicorn app.main:app --reload

8. Server dianggap berjalan jika kamu dapat mengakses link server yang keluar di terminal, contohnya:

    http://127.0.0.1:8000

=============================================================================================

**<div align=center>Migration Database</div>**

0. Untuk memastikan apakah migrasi database atau proses pembuatan table berserta colomnya berjalan dengan baik, maka anda bisa menjalankan perintah mysql,

    mysql> USE lamsia_db;

    // Perintah ini memilih database lamsia_db untuk dapat kita lakukan query (seperti show table)

    mysql> SHOW TABLES;
    +---------------------+
    | Tables_in_lamsia_db |
    +---------------------+
    | users               |
    +---------------------+

    // Jika table yang telah diprogramkan pada proyek, muncul pada perintah mysql tersebut, maka anda berhasil melakukan migrasi tabel
    // Selanjutnya, kita akan melakukan pengecekan coloum tabel, apakah telah sesuai dengan yang diprogram pada proyek,

    mysql> DESCRIBE users;
    +-----------+--------------+------+-----+---------+----------------+
    | Field     | Type         | Null | Key | Default | Extra          |
    +-----------+--------------+------+-----+---------+----------------+
    | id        | int          | NO   | PRI | NULL    | auto_increment |
    | username  | varchar(100) | NO   |     | NULL    |                |
    | telephone | varchar(100) | NO   |     | NULL    |                |
    | password  | varchar(255) | NO   |     | NULL    |                |
    +-----------+--------------+------+-----+---------+----------------+ 

    // Jika hasil output dari perintah mysql berupa tabel dengan kolom-kolom yang sesuai dengan yang diprogram di proyek, maka migrasi tabel dan kolom nya berhasil.

