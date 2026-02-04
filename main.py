import json
from datetime import date, timedelta

catatan = []
target_harian = None


def tambah_catatan():
    """Minta input mapel, topik, durasi (menit) dan simpan ke list `catatan`.

    Struktur yang digunakan: list berisi dictionary sederhana
    contoh: {'mapel': 'Matematika', 'topik': 'Aljabar', 'durasi': 60, 'tanggal': '2026-02-04'}
    """
    mapel = input("Masukkan mata pelajaran: ").strip()
    topik = input("Masukkan topik: ").strip()

    while True:
        durasi_input = input("Masukkan durasi belajar (menit): ").strip()
        try:
            durasi = int(durasi_input)
            if durasi <= 0:
                print("Durasi harus lebih dari 0. Coba lagi.")
                continue
            break
        except ValueError:
            print("Masukkan angka bulat untuk durasi. Coba lagi.")

    tanggal = date.today().isoformat()
    catatan.append({'mapel': mapel, 'topik': topik, 'durasi': durasi, 'tanggal': tanggal})
    print("Catatan berhasil ditambahkan!\n")


def lihat_catatan():
    """Tampilkan semua catatan dalam tabel sederhana.

    Jika belum ada data, tampilkan pesan yang sesuai.
    """
    if not catatan:
        print("Belum ada catatan belajar.")
        return

    # Tentukan lebar kolom berdasarkan data
    no_w = len(str(len(catatan)))
    mapel_w = max(len("Mapel"), max(len(c['mapel']) for c in catatan))
    topik_w = max(len("Topik"), max(len(c['topik']) for c in catatan))
    tanggal_w = max(len("Tanggal"), max(len(c.get('tanggal', '')) for c in catatan))
    durasi_w = max(len("Durasi"), max(len(str(c['durasi'])) for c in catatan))

    # Header
    print("\n=== Daftar Catatan ===")
    header = f"{'No'.ljust(no_w)}  {'Tanggal'.ljust(tanggal_w)}  {'Mapel'.ljust(mapel_w)}  {'Topik'.ljust(topik_w)}  {'Durasi'.rjust(durasi_w)}"
    print(header)
    print('-' * len(header))

    # Baris data
    for i, c in enumerate(catatan, start=1):
        no = str(i).ljust(no_w)
        tanggal = c.get('tanggal', '').ljust(tanggal_w)
        mapel = c['mapel'].ljust(mapel_w)
        topik = c['topik'].ljust(topik_w)
        durasi = str(c['durasi']).rjust(durasi_w)
        print(f"{no}  {tanggal}  {mapel}  {topik}  {durasi} menit")

    print(f"\nTotal catatan: {len(catatan)}")


def total_waktu():
    if not catatan:
        print("Belum ada catatan belajar.")
        return

    total = sum(c['durasi'] for c in catatan)
    jam = total // 60
    menit = total % 60
    if jam > 0:
        print(f"Total waktu belajar: {total} menit ({jam} jam {menit} menit)")
    else:
        print(f"Total waktu belajar: {total} menit")


def mapel_favorit():
    if not catatan:
        print("Belum ada catatan belajar.")
        return
    totals = {}
    for c in catatan:
        totals[c['mapel']] = totals.get(c['mapel'], 0) + c['durasi']
    favorit = max(totals.items(), key=lambda x: x[1])
    print(f"Mapel favorit: {favorit[0]} ({favorit[1]} menit belajar total)")


def filter_per_mapel():
    if not catatan:
        print("Belum ada catatan belajar.")
        return
    m = input("Masukkan nama mapel untuk filter: ").strip()
    hasil = [c for c in catatan if c['mapel'].lower() == m.lower()]
    if not hasil:
        print(f"Tidak ada catatan untuk mapel '{m}'.")
        return
    print(f"\nCatatan untuk mapel '{m}':")
    for i, c in enumerate(hasil, start=1):
        print(f"{i}. {c['tanggal']} - {c['topik']} ({c['durasi']} menit)")


def set_target_harian():
    global target_harian
    while True:
        inp = input("Masukkan target harian (menit), atau kosong untuk batal: ").strip()
        if inp == "":
            print("Batal mengatur target.")
            return
        try:
            t = int(inp)
            if t <= 0:
                print("Masukkan angka lebih dari 0.")
                continue
            target_harian = t
            print(f"Target harian diset ke {target_harian} menit.")
            return
        except ValueError:
            print("Masukkan angka bulat untuk target.")


def cek_target_harian():
    if target_harian is None:
        print("Belum ada target harian.")
        return
    hari_ini = date.today().isoformat()
    total_hari_ini = sum(c['durasi'] for c in catatan if c.get('tanggal') == hari_ini)
    print(f"Target: {target_harian} menit. Sudah: {total_hari_ini} menit.")
    if total_hari_ini >= target_harian:
        print("Selamat — target harian tercapai!")


def simpan_ke_file():
    nama = input("Nama file untuk menyimpan (enter = catatan.json): ").strip() or "catatan.json"
    try:
        with open(nama, 'w', encoding='utf-8') as f:
            json.dump(catatan, f, ensure_ascii=False, indent=2)
        print(f"Berhasil menyimpan ke {nama}")
    except Exception as e:
        print(f"Gagal menyimpan file: {e}")


def ringkasan_mingguan():
    if not catatan:
        print("Belum ada catatan belajar.")
        return
    today = date.today()
    days = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    totals_per_day = {d: 0 for d in days}
    for c in catatan:
        t = c.get('tanggal')
        if t in totals_per_day:
            totals_per_day[t] += c['durasi']
    print("\nRingkasan 7 hari terakhir:")
    for d in days:
        print(f"{d}: {totals_per_day[d]} menit")
    total_minggu = sum(totals_per_day.values())
    jam = total_minggu // 60
    menit = total_minggu % 60
    print(f"Total minggu ini: {total_minggu} menit ({jam} jam {menit} menit)")


def menu():
    print("\n=== Study Log App ===")
    print("1. Tambah catatan belajar")
    print("2. Lihat catatan belajar")
    print("3. Total waktu belajar")
    print("4. Mapel favorit")
    print("5. Filter per mapel")
    print("6. Target harian")
    print("7. Simpan ke file")
    print("8. Ringkasan mingguan")
    print("9. Keluar")


while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_catatan()
    elif pilihan == "2":
        lihat_catatan()
    elif pilihan == "3":
        total_waktu()
    elif pilihan == "4":
        mapel_favorit()
    elif pilihan == "5":
        filter_per_mapel()
    elif pilihan == "6":
        # menu target: bisa set atau cek
        sub = input("(s)et target atau (c)ek status? ").strip().lower()
        if sub == 's':
            set_target_harian()
        else:
            cek_target_harian()
    elif pilihan == "7":
        simpan_ke_file()
    elif pilihan == "8":
        ringkasan_mingguan()
    elif pilihan == "9":
        print("Terima kasih, terus semangat belajar!")
        break
    else:
        print("Pilihan tidak valid")