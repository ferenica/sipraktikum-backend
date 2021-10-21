from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from authentication.role import Role
from laporan_praktikum.models import (
    Praktikum,
    MahasiswaPraktikum,
    KelolaLaporanPraktikum,
    LaporanAkhirPraktikum,
    LaporanBorangPraktikum
)
from lembaga.models import (
    Institusi,
    Tema,
    Lembaga,
)
from authentication.models import (
    User,
    Mahasiswa,
    SupervisorLembaga,
    SupervisorSekolah,
    KoordinatorKuliah,
    Administrator,
    Periode,
    ORG_CODE,
)
import os
import django
import random
import string
import datetime
import base64


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sip.settings.staging")
django.setup()


def seed_user(user_number_each_role):
    role_mhs = [(Role.MHS, Role.MHS.value)] * 4
    roles = [(tag, tag.value) for tag in Role] + role_mhs
    roles = roles * user_number_each_role
    for i in range(len(roles)):
        user_data = 'user' + str(i)
        User.objects.create_user(
            username='username_' + user_data,
            email='email_' + user_data + '@mail.com',
            password='password_' + user_data,
            full_name='full_name_' + user_data,
            role=roles[i][1]
        )
    print('seeding user..... [SUCCESS]')


def seed_institusi(institusi_number):
    Institusi.objects.create(nama='Government Organisation')
    Institusi.objects.create(nama='Non Government Organisation')
    Institusi.objects.create(nama='Komunitas')
    Institusi.objects.create(nama='Perusahaan')
    Institusi.objects.create(nama='Pendidikan')
    print('seeding institusi..... [SUCCESS]')


def seed_tema(tema_number):
    Tema.objects.create(nama='Lingkungan')
    Tema.objects.create(nama='HRD')
    Tema.objects.create(nama='CSR ')
    Tema.objects.create(nama='Anak dan Remaja')
    Tema.objects.create(nama='Lansia')
    Tema.objects.create(nama='Disabilitas')
    Tema.objects.create(nama='Gender/Perempuan')
    Tema.objects.create(nama='Pemberdayaan Masyarakat')
    Tema.objects.create(nama='Penanganan Kemiskinan')
    Tema.objects.create(nama='Kesehatan')
    print('seeding tema..... [SUCCESS]')


def seed_lembaga(lembaga_number):
    all_institusi = Institusi.objects.all()
    all_tema = Tema.objects.all()
    jenis_pelayanan_list = [
        'Perusahaan',
        'Pemerintahan',
        'Organisasi',
    ]
    for i in range(lembaga_number):
        lembaga = Lembaga.objects.create(
            nama='nama_lembaga_' + str(i),
            jenis_pelayanan=random.choice(jenis_pelayanan_list),
            institusi=random.choice(all_institusi),
            tema=random.choice(all_tema),
            deskripsi_singkat='deskripsi_singkat_' + str(i),
            praktikum_ke=1,
            beneficaries="test_beneficaries_" + str(i),
            alamat="test_alamat_" + str(i)
        )
        lembaga.save()
    print('seeding lembaga..... [SUCCESS]')


def seed_supervisor_lembaga():
    users = User.objects.filter(role=Role.SLB.value)
    all_lembaga = Lembaga.objects.all()
    jabatan_list = [
        'direktur',
        'ketua',
        'hrd',
        'senior marketing',
        'associate marketing'
    ]
    for i in range(len(users)):
        SupervisorLembaga.objects.create(
            jabatan=random.choice(jabatan_list),
            lembaga=random.choice(all_lembaga),
            user=users[i]
        )
    print('seeding supervisor lembaga..... [SUCCESS]')


def seed_supervisor_sekolah():
    users = User.objects.filter(role=Role.SSK.value)
    for i in range(len(users)):
        SupervisorSekolah.objects.create(
            nip=random.randint(100000000000, 199999999999),
            user=users[i]
        )
    print('seeding supervisor sekolah..... [SUCCESS]')


def seed_koordinator_kuliah():
    users = User.objects.filter(role=Role.KKL.value)
    for i in range(len(users)):
        KoordinatorKuliah.objects.create(
            nip=random.randint(100000000000, 199999999999),
            user=users[i]
        )
    print('seeding koordinator kuliah..... [SUCCESS]')


def seed_administrator():
    users = User.objects.filter(role=Role.ADM.value)
    for i in range(len(users)):
        Administrator.objects.create(
            nip=random.randint(100000000000, 199999999999),
            user=users[i]
        )
    print('seeding administrator..... [SUCCESS]')


def seed_periode():
    periode_list = [
        '2018/2019 - Gasal',
        '2018/2019 - Genap',
        '2019/2020 - Gasal',
        '2020/2021 - Genap',
        '2020/2021 - Gasal'
    ]
    for i in range(len(periode_list)):
        Periode.objects.create(
            nama=periode_list[i]
        )
    print('seeding periode..... [SUCCESS]')


def seed_mahasiswa():
    org_code_list = [
        '02.07.09.01',
        '05.03.09.01',
        '06.03.09.01',
        '07.03.09.01',
        '01.08.09.01',
        '01.06.09.01',
        '02.01.09.01',
        '01.02.09.01',
        '01.05.09.01',
        '01.04.09.01',
        '07.01.09.01'
    ]
    users = User.objects.filter(role=Role.MHS.value)
    supervisor_lembaga = SupervisorLembaga.objects.all()
    supervisor_sekolah = SupervisorSekolah.objects.all()
    periode_list = Periode.objects.all()

    for i in range(len(users)):
        org_code_random = random.choice(org_code_list)
        Mahasiswa.objects.create(
            org_code='org_code' + str(i),
            faculty=ORG_CODE['id'][org_code_random]['faculty'],
            major=ORG_CODE['id'][org_code_random]['faculty'],
            program=ORG_CODE['id'][org_code_random]['faculty'],
            npm=random.randint(1200000000, 1900000000),
            periode=random.choice(periode_list),
            user=users[i],
            supervisor_lembaga=supervisor_lembaga[i % len(supervisor_lembaga)],
            supervisor_sekolah=supervisor_sekolah[i % len(supervisor_sekolah)]
        )
    print('seeding mahasiswa..... [SUCCESS]')


def seed_superuser():
    User.objects.create_superuser(
        email='admin@ppl.com',
        password='secret123'
    )
    print('seeding super user..... [SUCCESS]')


def seed_praktikum():
    Praktikum.objects.create(
        jenis_praktikum="Praktikum 1"
    )
    Praktikum.objects.create(
        jenis_praktikum="Praktikum 2"
    )
    print('seeding praktikum..... [SUCCESS]')


def seed_kelola_laporan_praktikum(laporan_praktikum_number):
    mahasiswa = Mahasiswa.objects.all()

    for i in range(len(mahasiswa)):
        this_mahasiswa = mahasiswa[i]
        status_praktikum1 = True
        status_praktikum2 = False

        praktikum1 = Praktikum.objects.get(jenis_praktikum='Praktikum 1')
        praktikum2 = Praktikum.objects.get(jenis_praktikum='Praktikum 2')

        if i % 3 == 0:
            status_praktikum2 = True
            status_praktikum1 = False

        MahasiswaPraktikum.objects.create(
            mahasiswa=this_mahasiswa,
            list_praktikum=praktikum1,
            status=status_praktikum1
        )

        MahasiswaPraktikum.objects.create(
            mahasiswa=this_mahasiswa,
            list_praktikum=praktikum2,
            status=status_praktikum2
        )
        for i in range(0, 2):
            if i:
                this_praktikum = praktikum2
            else:
                this_praktikum = praktikum1
            for i in range(laporan_praktikum_number):
                random_year = 2020
                random_month = random.randint(1, 6)
                random_day = random.randint(1, 27)
                random_hour = random.randint(0, 22)
                random_minute = random.randint(0, 58)
                random_second = random.randint(0, 58)
                is_submitted = random.choice([True, False])
                if is_submitted:
                    KelolaLaporanPraktikum.objects.create(
                        nama_laporan='nama_laporan_' + str(i),
                        mahasiswa=this_mahasiswa,
                        jenis_praktikum=this_praktikum,
                        waktu_deadline=datetime.datetime(
                            random_year,
                            random_month,
                            random_day,
                            random_hour,
                            random_minute,
                            random_second
                        ),
                        waktu_submisi=datetime.datetime(
                            random_year,
                            random_month,
                            random_day + 1,
                            random_hour + 1,
                            random_minute + 1,
                            random_second + 1
                        ),
                        status_publikasi=True,
                        status_submisi=True,
                        skor_laporan_sekolah=random.randint(0, 100),
                        skor_laporan_lembaga=random.randint(0, 100),
                        link_submisi="https://link_submisi_" + str(i) + ".com"
                    )
                else:
                    KelolaLaporanPraktikum.objects.create(
                        nama_laporan='nama_laporan_' + str(i),
                        mahasiswa=this_mahasiswa,
                        jenis_praktikum=this_praktikum,
                        waktu_deadline=datetime.datetime(
                            random_year,
                            random_month,
                            random_day,
                            random_hour,
                            random_minute,
                            random_second
                        ),
                        status_publikasi=random.randint(False, True),
                        status_submisi=False,
                        skor_laporan_sekolah=-1,
                        skor_laporan_lembaga=-1
                    )
    print('seeding kelola laporan praktikum..... [SUCCESS]')


def seed_laporan_akhir_praktikum(laporan_praktikum_number):
    mahasiswa = Mahasiswa.objects.all()

    for i in range(len(mahasiswa)):
        this_mahasiswa = mahasiswa[i]
        status_praktikum1 = True
        status_praktikum2 = False

        praktikum1 = Praktikum.objects.get(jenis_praktikum='Praktikum 1')
        praktikum2 = Praktikum.objects.get(jenis_praktikum='Praktikum 2')

        if i % 3 == 0:
            status_praktikum2 = True
            status_praktikum1 = False

        for i in range(0, 2):
            if i:
                this_praktikum = praktikum2
            else:
                this_praktikum = praktikum1
            for i in range(laporan_praktikum_number):
                random_year = 2020
                random_month = random.randint(1, 6)
                random_day = random.randint(1, 27)
                random_hour = random.randint(0, 22)
                random_minute = random.randint(0, 58)
                random_second = random.randint(0, 58)
                is_submitted = random.choice([True, False])
                if is_submitted:
                    LaporanAkhirPraktikum.objects.create(
                        nama_laporan='nama_laporan_akhir' + str(i),
                        lembaga=None,
                        mahasiswa=this_mahasiswa,
                        jenis_praktikum=this_praktikum,
                        waktu_deadline=datetime.datetime(
                            random_year,
                            random_month,
                            random_day,
                            random_hour,
                            random_minute,
                            random_second
                        ),
                        waktu_submisi=datetime.datetime(
                            random_year,
                            random_month,
                            random_day + 1,
                            random_hour + 1,
                            random_minute + 1,
                            random_second + 1
                        ),
                        status_publikasi=True,
                        status_submisi=True,
                        periode_praktikum="2019/2020",
                        laporan_akhir=SimpleUploadedFile("laporan_akhir_{}.pdf".format(str(i)), b"These are the file contents!"),
                        profil_lembaga=SimpleUploadedFile("profil_lembaga_{}.pdf".format(str(i)), b"These are the file contents!"),
                        umpan_balik=" "
                    )
                else:
                    LaporanAkhirPraktikum.objects.create(
                        nama_laporan='nama_laporan_akhir' + str(i),
                        lembaga=None,
                        mahasiswa=this_mahasiswa,
                        jenis_praktikum=this_praktikum,
                        waktu_deadline=datetime.datetime(
                            random_year,
                            random_month,
                            random_day,
                            random_hour,
                            random_minute,
                            random_second
                        ),
                        status_publikasi=random.randint(False, True),
                        status_submisi=False,
                        periode_praktikum=" ",
                        laporan_akhir=None,
                        profil_lembaga=None,
                        umpan_balik=" "
                    )
    print('seeding laporan akhir praktikum..... [SUCCESS]')


def seed_laporan_borang_praktikum(laporan_praktikum_number):
    mahasiswa = Mahasiswa.objects.all()

    for i in range(len(mahasiswa)):
        this_mahasiswa = mahasiswa[i]
        status_praktikum1 = True
        status_praktikum2 = False

        praktikum1 = Praktikum.objects.get(jenis_praktikum='Praktikum 1')
        praktikum2 = Praktikum.objects.get(jenis_praktikum='Praktikum 2')

        if i % 3 == 0:
            status_praktikum2 = True
            status_praktikum1 = False

        for i in range(0, 2):
            if i:
                this_praktikum = praktikum2
            else:
                this_praktikum = praktikum1
            for i in range(laporan_praktikum_number):
                random_year = 2020
                random_month = random.randint(1, 6)
                random_day = random.randint(1, 27)
                random_hour = random.randint(0, 22)
                random_minute = random.randint(0, 58)
                random_second = random.randint(0, 58)
                is_submitted = random.choice([True, False])
                if is_submitted:
                    LaporanBorangPraktikum.objects.create(
                        nama_laporan='nama_laporan_borang' + str(i),
                        mahasiswa=this_mahasiswa,
                        jenis_praktikum=this_praktikum,
                        waktu_deadline=datetime.datetime(
                            random_year,
                            random_month,
                            random_day,
                            random_hour,
                            random_minute,
                            random_second
                        ),
                        waktu_submisi=datetime.datetime(
                            random_year,
                            random_month,
                            random_day + 1,
                            random_hour + 1,
                            random_minute + 1,
                            random_second + 1
                        ),
                        status_publikasi=True,
                        status_submisi=True,
                        borang_supv_sekolah=SimpleUploadedFile("laporan_borang_supv_sekolah_{}.pdf".format(str(i)), b"These are the file contents!"),
                        borang_supv_lembaga=SimpleUploadedFile("laporan_borang_supv_lembaga_{}.pdf".format(str(i)), b"These are the file contents!"),
                        borang_supv_perkuliahan=SimpleUploadedFile("laporan_borang_supv_perkuliahan_{}.pdf".format(str(i)), b"These are the file contents!"),
                    )
                else:
                    LaporanBorangPraktikum.objects.create(
                        nama_laporan='nama_laporan_borang' + str(i),
                        mahasiswa=this_mahasiswa,
                        jenis_praktikum=this_praktikum,
                        waktu_deadline=datetime.datetime(
                            random_year,
                            random_month,
                            random_day,
                            random_hour,
                            random_minute,
                            random_second
                        ),
                        status_publikasi=random.randint(False, True),
                        status_submisi=False,
                    )
    print('seeding laporan borang praktikum..... [SUCCESS]')


if __name__ == "__main__":
    user_number_each_role = 2
    lembaga_number = 5
    laporan_praktikum_number = 3
    laporan_akhir_number = 1
    laporan_borang_number = 1

    seed_institusi(lembaga_number)
    seed_tema(lembaga_number)
    seed_lembaga(lembaga_number)
    seed_periode()

    seed_user(user_number_each_role)
    seed_supervisor_lembaga()
    seed_supervisor_sekolah()
    seed_koordinator_kuliah()
    seed_administrator()
    seed_mahasiswa()
    seed_superuser()

    seed_praktikum()
    seed_kelola_laporan_praktikum(laporan_praktikum_number)
    seed_laporan_akhir_praktikum(laporan_akhir_number)
    seed_laporan_borang_praktikum(laporan_borang_number)
