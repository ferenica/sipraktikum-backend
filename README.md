# MKPPL-SI Penilaian dan Evaluasi Praktikum



## __Getting Started__
Pastikan **python3** dan **git** sudah terinstall pada laptop/komputer Anda.
```bash
git clone https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2020/mkppl-si-penilaian-dan-evaluasi-praktikum.git
cd mkppl-si-penilaian-dan-evaluasi-praktikum
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## __Setup Local__

### Settings Directory Tree
```
...
+-- sip
|   +-- settings
|   |   +-- static (generated)
|   |   +-- dev.py (for local)
|   |   +-- production.py (for production)
|   |   +-- staging.py (for staging)
|
...
```
### __Environment Variables__
Contoh bentuk file `.env.dev`, ini akan di-*load* pada `settings/dev.py`
***Catatan: file ini dapat berubah menyesuaikan flow, ini hanya contoh.***
```
SECRET_KEY="sm1l3_sw33t_s1st3r_sUrpr1s3_s3rvc1c3"
DB_NAME=db_name
DB_USER=admin
DB_PASS=db_password
DB_HOST=db
DB_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=postgres_db_name
```

### __How To Run on Local Development__
1. Buat .env di folder sip/settings/ dengan secret key-nya. Tambahin line ini di file-nya:
    ```bash
    DJANGO_SECRET_KEY="s3cr3t_k3y_c4nn0t_h4ck3d_by_l33t_1337"
    ```
2. Lakukan makemigrations dan migrate
    ```bash
    python manage.py makemigrations --settings=sip.settings.dev
    python manage.py migrate --settings=sip.settings.dev
    ```
3. Jalankan aplikasi menggunakan `manage.py runserver` pada port 8000, spesifikasi settings yang digunakan adalah `dev` atau local.
    ```bash
    python manage.py runserver 8000 --settings=<path>.sip.settings.dev
    ```

### __Pipelines and Coverage__
[![pipeline status](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2021/BB/departemen-ilmu-kesejahteraan-sosial-ui-sistem-informasi-penilaian-dan-database-praktikum-i-dan-ii/praktikum-backend/badges/staging/pipeline.svg)](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2021/BB/departemen-ilmu-kesejahteraan-sosial-ui-sistem-informasi-penilaian-dan-database-praktikum-i-dan-ii/praktikum-backend/commits/staging/) 
[![coverage report](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2021/BB/departemen-ilmu-kesejahteraan-sosial-ui-sistem-informasi-penilaian-dan-database-praktikum-i-dan-ii/praktikum-backend/badges/staging/coverage.svg)](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2021/BB/departemen-ilmu-kesejahteraan-sosial-ui-sistem-informasi-penilaian-dan-database-praktikum-i-dan-ii/praktikum-backend/commits/staging/)

