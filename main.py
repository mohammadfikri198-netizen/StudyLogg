catatan = []

def tambah_catatan():
    """Minta input mapel, topik, durasi (menit) dan simpan ke list `catatan`.

    Struktur yang digunakan: list berisi dictionary sederhana
    contoh: {'mapel': 'Matematika', 'topik': 'Aljabar', 'durasi': 60}
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

    catatan.append({'mapel': mapel, 'topik': topik, 'durasi': durasi})
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
    durasi_w = max(len("Durasi"), max(len(str(c['durasi'])) for c in catatan))

    # Header
    print("\n=== Daftar Catatan ===")
    header = f"{'No'.ljust(no_w)}  {'Mapel'.ljust(mapel_w)}  {'Topik'.ljust(topik_w)}  {'Durasi'.rjust(durasi_w)}"
    print(header)
    print('-' * len(header))

    # Baris data
    for i, c in enumerate(catatan, start=1):
        no = str(i).ljust(no_w)
        mapel = c['mapel'].ljust(mapel_w)
        topik = c['topik'].ljust(topik_w)
        durasi = str(c['durasi']).rjust(durasi_w)
        print(f"{no}  {mapel}  {topik}  {durasi} menit")

    print(f"\nTotal catatan: {len(catatan)}")

def total_waktu():
    if not catatan:
        print("Belum ada catatan belajar.")
        return
    total = sum(c['durasi'] for c in catatan)
    print(f"Total waktu belajar: {total} menit")

def menu():
    print("\n=== Study Log App ===")
    print("1. Tambah catatan belajar")
    print("2. Lihat catatan belajar")
    print("3. Total waktu belajar")
    print("4. Keluar")

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
        print("Terima kasih, terus semangat belajar!")
        break
    else:
        print("Pilihan tidak valid")