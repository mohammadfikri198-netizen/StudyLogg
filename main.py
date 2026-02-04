import json
import csv
from datetime import date, timedelta

catatan = []
target_harian = None


def tambah_catatan():
    """Minta input mapel, topik, durasi (menit), rating dan simpan ke list `catatan`.

    Struktur: {'mapel': str, 'topik': str, 'durasi': int, 'rating': int (1-5), 'tanggal': str}
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

    while True:
        rating_input = input("Rating kepuasan belajar (1-5, atau kosong untuk skip): ").strip()
        if rating_input == "":
            rating = 3  # default
            break
        try:
            rating = int(rating_input)
            if rating < 1 or rating > 5:
                print("Rating harus antara 1-5.")
                continue
            break
        except ValueError:
            print("Masukkan angka bulat.")

    tanggal = date.today().isoformat()
    catatan.append({'mapel': mapel, 'topik': topik, 'durasi': durasi, 'rating': rating, 'tanggal': tanggal})
    print("Catatan berhasil ditambahkan!\n")


def lihat_catatan():
    """Tampilkan semua catatan dalam tabel sederhana dengan rating."""
    if not catatan:
        print("Belum ada catatan belajar.")
        return

    no_w = len(str(len(catatan)))
    mapel_w = max(len("Mapel"), max(len(c['mapel']) for c in catatan))
    topik_w = max(len("Topik"), max(len(c['topik']) for c in catatan))
    tanggal_w = len("Tanggal")
    durasi_w = max(len("Durasi"), max(len(str(c['durasi'])) for c in catatan))

    print("\n=== Daftar Catatan ===")
    header = f"{'No'.ljust(no_w)}  {'Tanggal'.ljust(tanggal_w)}  {'Mapel'.ljust(mapel_w)}  {'Topik'.ljust(topik_w)}  {'Durasi'.rjust(durasi_w)}  Rating"
    print(header)
    print('-' * len(header))

    for i, c in enumerate(catatan, start=1):
        no = str(i).ljust(no_w)
        tanggal = c.get('tanggal', '').ljust(tanggal_w)
        mapel = c['mapel'].ljust(mapel_w)
        topik = c['topik'].ljust(topik_w)
        durasi = str(c['durasi']).rjust(durasi_w)
        rating = '⭐' * c.get('rating', 3)
        print(f"{no}  {tanggal}  {mapel}  {topik}  {durasi} menit  {rating}")

    print(f"\nTotal catatan: {len(catatan)}")


def hapus_catatan():
    """Hapus catatan berdasarkan nomor urut."""
    if not catatan:
        print("Belum ada catatan belajar.")
        return
    
    lihat_catatan()
    while True:
        try:
            nomor = int(input("Masukkan nomor catatan yang ingin dihapus (0 untuk batal): "))
            if nomor == 0:
                print("Batal menghapus.")
                return
            if 1 <= nomor <= len(catatan):
                deleted = catatan.pop(nomor - 1)
                print(f"Catatan '{deleted['topik']}' berhasil dihapus.")
                return
            print(f"Nomor harus antara 1-{len(catatan)}.")
        except ValueError:
            print("Masukkan angka bulat.")


def edit_catatan():
    """Edit catatan berdasarkan nomor urut."""
    if not catatan:
        print("Belum ada catatan belajar.")
        return
    
    lihat_catatan()
    while True:
        try:
            nomor = int(input("Masukkan nomor catatan yang ingin diedit (0 untuk batal): "))
            if nomor == 0:
                print("Batal mengedit.")
                return
            if 1 <= nomor <= len(catatan):
                break
            print(f"Nomor harus antara 1-{len(catatan)}.")
        except ValueError:
            print("Masukkan angka bulat.")
    
    c = catatan[nomor - 1]
    print(f"\nEdit catatan: {c['topik']}")
    mapel = input(f"Mapel [{c['mapel']}]: ").strip() or c['mapel']
    topik = input(f"Topik [{c['topik']}]: ").strip() or c['topik']
    
    while True:
        durasi_input = input(f"Durasi [{c['durasi']} menit]: ").strip() or str(c['durasi'])
        try:
            durasi = int(durasi_input)
            if durasi > 0:
                break
            print("Durasi harus lebih dari 0.")
        except ValueError:
            print("Masukkan angka bulat.")
    
    while True:
        rating_input = input(f"Rating [{c.get('rating', 3)}]: ").strip() or str(c.get('rating', 3))
        try:
            rating = int(rating_input)
            if 1 <= rating <= 5:
                break
            print("Rating harus antara 1-5.")
        except ValueError:
            print("Masukkan angka bulat.")
    
    catatan[nomor - 1] = {'mapel': mapel, 'topik': topik, 'durasi': durasi, 'rating': rating, 'tanggal': c['tanggal']}
    print("Catatan berhasil diperbarui.\n")


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
    print(f"\n=== Catatan untuk Mapel '{m}' ===")
    
    no_w = len(str(len(hasil)))
    tanggal_w = len("Tanggal")
    topik_w = max(len("Topik"), max(len(c['topik']) for c in hasil))
    durasi_w = 8
    
    header = f"{'No'.ljust(no_w)}  {'Tanggal'.ljust(tanggal_w)}  {'Topik'.ljust(topik_w)}  {'Durasi'.rjust(durasi_w)}  Rating"
    print(header)
    print('-' * len(header))
    
    for i, c in enumerate(hasil, start=1):
        rating = '⭐' * c.get('rating', 3)
        no = str(i).ljust(no_w)
        tanggal = c['tanggal'].ljust(tanggal_w)
        topik = c['topik'].ljust(topik_w)
        durasi = str(c['durasi']).rjust(durasi_w)
        print(f"{no}  {tanggal}  {topik}  {durasi} menit  {rating}")


def statistik_detail_mapel():
    """Tampilkan statistik detail per mata pelajaran."""
    if not catatan:
        print("Belum ada catatan belajar.")
        return
    
    stats = {}
    for c in catatan:
        m = c['mapel']
        if m not in stats:
            stats[m] = {'total': 0, 'count': 0, 'ratings': []}
        stats[m]['total'] += c['durasi']
        stats[m]['count'] += 1
        stats[m]['ratings'].append(c.get('rating', 3))
    
    print("\n=== Statistik Detail Per Mapel ===")
    
    mapel_w = max(len("Mapel"), max(len(m) for m in stats.keys()))
    durasi_w = 20
    topik_w = 12
    rating_w = 10
    
    header = f"{'Mapel'.ljust(mapel_w)}  {'Total Durasi'.ljust(durasi_w)}  {'Topik'.ljust(topik_w)}  Rating"
    print(header)
    print('-' * (mapel_w + durasi_w + topik_w + rating_w + 6))
    
    for mapel in sorted(stats.keys()):
        s = stats[mapel]
        avg_rating = sum(s['ratings']) / len(s['ratings'])
        durasi_str = f"{s['total']} menit ({s['total']//60}h {s['total']%60}m)"
        rating_str = f"{avg_rating:.1f}⭐"
        print(f"{mapel.ljust(mapel_w)}  {durasi_str.ljust(durasi_w)}  {str(s['count']).ljust(topik_w)}  {rating_str.ljust(rating_w)}")


def ranking_mapel():
    """Tampilkan ranking mapel berdasarkan durasi belajar."""
    if not catatan:
        print("Belum ada catatan belajar.")
        return
    
    totals = {}
    for c in catatan:
        totals[c['mapel']] = totals.get(c['mapel'], 0) + c['durasi']
    
    sorted_mapel = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    print("\n=== Ranking Mapel ===")
    
    rank_w = len(str(len(sorted_mapel)))
    mapel_w = max(len("Mapel"), max(len(m[0]) for m in sorted_mapel))
    durasi_w = 20
    
    header = f"{'Rank'.ljust(rank_w)}  {'Mapel'.ljust(mapel_w)}  {'Total Durasi'.ljust(durasi_w)}"
    print(header)
    print('-' * (rank_w + mapel_w + durasi_w + 4))
    
    for i, (mapel, durasi) in enumerate(sorted_mapel, start=1):
        durasi_str = f"{durasi} menit ({durasi//60}h {durasi%60}m)"
        print(f"{str(i).ljust(rank_w)}  {mapel.ljust(mapel_w)}  {durasi_str.ljust(durasi_w)}")


def cari_topik():
    """Cari catatan berdasarkan topik atau kata kunci."""
    if not catatan:
        print("Belum ada catatan belajar.")
        return
    
    keyword = input("Masukkan kata kunci untuk mencari topik: ").strip().lower()
    hasil = [c for c in catatan if keyword in c['topik'].lower()]
    
    if not hasil:
        print(f"Tidak ada catatan dengan topik yang mengandung '{keyword}'.")
        return
    
    print(f"\n=== Hasil Pencarian '{keyword}' ===")
    
    no_w = len(str(len(hasil)))
    mapel_w = max(len("Mapel"), max(len(c['mapel']) for c in hasil))
    topik_w = max(len("Topik"), max(len(c['topik']) for c in hasil))
    tanggal_w = len("Tanggal")
    durasi_w = 8
    
    header = f"{'No'.ljust(no_w)}  {'Tanggal'.ljust(tanggal_w)}  {'Mapel'.ljust(mapel_w)}  {'Topik'.ljust(topik_w)}  {'Durasi'.rjust(durasi_w)}  Rating"
    print(header)
    print('-' * len(header))
    
    for i, c in enumerate(hasil, start=1):
        rating = '⭐' * c.get('rating', 3)
        no = str(i).ljust(no_w)
        tanggal = c['tanggal'].ljust(tanggal_w)
        mapel = c['mapel'].ljust(mapel_w)
        topik = c['topik'].ljust(topik_w)
        durasi = str(c['durasi']).rjust(durasi_w)
        print(f"{no}  {tanggal}  {mapel}  {topik}  {durasi} menit  {rating}")


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
    """Simpan catatan ke file JSON."""
    nama = input("Nama file untuk menyimpan (enter = catatan.json): ").strip() or "catatan.json"
    try:
        with open(nama, 'w', encoding='utf-8') as f:
            json.dump(catatan, f, ensure_ascii=False, indent=2)
        print(f"Berhasil menyimpan ke {nama}")
    except Exception as e:
        print(f"Gagal menyimpan file: {e}")


def import_dari_file():
    """Import catatan dari file JSON."""
    global catatan
    nama = input("Nama file untuk dibaca (enter = catatan.json): ").strip() or "catatan.json"
    try:
        with open(nama, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            catatan = data
            print(f"Berhasil mengimpor {len(catatan)} catatan dari {nama}")
        else:
            print("Format file tidak valid.")
    except FileNotFoundError:
        print(f"File '{nama}' tidak ditemukan.")
    except Exception as e:
        print(f"Gagal membaca file: {e}")


def export_ke_csv():
    """Export catatan ke file CSV."""
    if not catatan:
        print("Belum ada catatan belajar.")
        return
    
    nama = input("Nama file CSV untuk disimpan (enter = catatan.csv): ").strip() or "catatan.csv"
    try:
        with open(nama, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['mapel', 'topik', 'durasi', 'rating', 'tanggal'])
            writer.writeheader()
            writer.writerows(catatan)
        print(f"Berhasil mengekspor ke {nama}")
    except Exception as e:
        print(f"Gagal mengekspor file: {e}")


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
    print("\n=== Ringkasan 7 Hari Terakhir ===")
    tanggal_w = len("Tanggal")
    durasi_w = 15
    
    header = f"{'Tanggal'.ljust(tanggal_w)}  {'Durasi Belajar'.ljust(durasi_w)}"
    print(header)
    print('-' * (tanggal_w + durasi_w + 2))
    
    for d in days:
        durasi_str = f"{totals_per_day[d]} menit"
        print(f"{d.ljust(tanggal_w)}  {durasi_str.ljust(durasi_w)}")
    
    total_minggu = sum(totals_per_day.values())
    jam = total_minggu // 60
    menit = total_minggu % 60
    print('-' * (tanggal_w + durasi_w + 2))
    print(f"{'TOTAL'.ljust(tanggal_w)}  {total_minggu} menit ({jam} jam {menit} menit)")


def hitung_streak():
    """Hitung berapa hari berturut-turut belajar (konsistensi)."""
    if not catatan:
        print("Belum ada catatan belajar.")
        return
    
    hari_unik = sorted(set(c.get('tanggal') for c in catatan))
    
    if not hari_unik:
        print("Belum ada tanggal catatan.")
        return
    
    # Hitung streak terpanjang dan streak saat ini
    streak_max = 1
    streak_saat_ini = 1
    
    for i in range(1, len(hari_unik)):
        prev = date.fromisoformat(hari_unik[i-1])
        curr = date.fromisoformat(hari_unik[i])
        delta = (curr - prev).days
        
        if delta == 1:
            streak_saat_ini += 1
            streak_max = max(streak_max, streak_saat_ini)
        elif delta > 1:
            streak_saat_ini = 1
    
    hari_terakhir = date.fromisoformat(hari_unik[-1])
    hari_ini = date.today()
    delta_terakhir = (hari_ini - hari_terakhir).days
    
    if delta_terakhir == 0:
        streak_aktif = streak_saat_ini
    elif delta_terakhir == 1:
        streak_aktif = streak_saat_ini
    else:
        streak_aktif = 0
    
    print(f"\n=== Streak Konsistensi Belajar ===")
    
    label_w = 20
    value_w = 15
    
    header = f"{'Metrik'.ljust(label_w)}  {'Nilai'.ljust(value_w)}"
    print(header)
    print('-' * (label_w + value_w + 2))
    
    print(f"{'Streak terpanjang'.ljust(label_w)}  {(str(streak_max) + ' hari').ljust(value_w)}")
    print(f"{'Streak saat ini'.ljust(label_w)}  {(str(streak_aktif) + ' hari').ljust(value_w)}")
    
    if streak_aktif > 0:
        status = "Aktif 🔥"
    else:
        status = "Mulai hari ini"
    print(f"{'Status'.ljust(label_w)}  {status.ljust(value_w)}")


def menu():
    print("\n=== Study Log App ===")
    print("1. Tambah catatan belajar")
    print("2. Lihat catatan belajar")
    print("3. Hapus catatan")
    print("4. Edit catatan")
    print("5. Cari topik")
    print("6. Total waktu belajar")
    print("7. Mapel favorit")
    print("8. Filter per mapel")
    print("9. Statistik detail mapel")
    print("10. Ranking mapel")
    print("11. Target harian")
    print("12. Streak konsistensi")
    print("13. Ringkasan mingguan")
    print("14. Simpan ke file")
    print("15. Import dari file")
    print("16. Export ke CSV")
    print("17. Keluar")


while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_catatan()
    elif pilihan == "2":
        lihat_catatan()
    elif pilihan == "3":
        hapus_catatan()
    elif pilihan == "4":
        edit_catatan()
    elif pilihan == "5":
        cari_topik()
    elif pilihan == "6":
        total_waktu()
    elif pilihan == "7":
        mapel_favorit()
    elif pilihan == "8":
        filter_per_mapel()
    elif pilihan == "9":
        statistik_detail_mapel()
    elif pilihan == "10":
        ranking_mapel()
    elif pilihan == "11":
        sub = input("(s)et target atau (c)ek status? ").strip().lower()
        if sub == 's':
            set_target_harian()
        else:
            cek_target_harian()
    elif pilihan == "12":
        hitung_streak()
    elif pilihan == "13":
        ringkasan_mingguan()
    elif pilihan == "14":
        simpan_ke_file()
    elif pilihan == "15":
        import_dari_file()
    elif pilihan == "16":
        export_ke_csv()
    elif pilihan == "17":
        print("Terima kasih, terus semangat belajar!")
        break
    else:
        print("Pilihan tidak valid")
