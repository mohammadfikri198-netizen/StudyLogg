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
    if not catatan:
        print("Belum ada catatan belajar.")
        return
    print("\n=== Daftar Catatan ===")
    for i, c in enumerate(catatan, start=1):
        print(f"{i}. {c['mapel']} - {c['topik']} ({c['durasi']} menit)")

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