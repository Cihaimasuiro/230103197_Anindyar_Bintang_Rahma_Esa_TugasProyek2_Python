# Nama: Anindyar Bintang Rahma Esa
# NIM : 230103197
# Proyek: student_performance_tracker
# File: app.py (Controller Utama / Menu CLI)

import csv
from pathlib import Path

# Impor modular dari paket 'tracker' yang sudah kita buat
try:
    from tracker import (
        Mahasiswa,
        RekapKelas,
        build_markdown_report,
        save_text
    )
except ImportError:
    print("Error: Pastikan file __init__.py ada di dalam folder 'tracker/'")
    print("Dan semua file (mahasiswa.py, dll.) ada di dalamnya.")
    exit()

# --- Fungsi Helper untuk Memuat Data ---

def load_csv(path_str):
    """Membaca file CSV dan mengembalikan list of dictionaries."""
    p = Path(path_str)
    if not p.exists():
        raise FileNotFoundError(f"File data tidak ditemukan di: {p.resolve()}")
    
    with p.open('r', encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

def bootstrap_from_csv(rekap, att_path="data/attendance.csv", grd_path="data/grades.csv"):
    """
    Mengisi objek RekapKelas dengan data dari file CSV kehadiran dan nilai.
    Fungsi ini diambil dan diadaptasi dari materi praktek M9/M10.
    """
    print(f"Memuat data dari {att_path} dan {grd_path}...")
    try:
        data_hadir = load_csv(att_path)
        data_nilai = load_csv(grd_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Error saat membaca CSV: {e}")
        return

    # 1. Buat objek Mahasiswa dari file kehadiran
    for row in data_hadir:
        try:
            nim = row["student_id"]
            nama = row["name"]
            m = Mahasiswa(nim, nama)
            rekap.tambah_mahasiswa(m)

            # Hitung persentase kehadiran
            weeks = [k for k in row.keys() if k.startswith("week")]
            if weeks:
                total_minggu = len(weeks)
                total_hadir = sum(int(row[w].strip() or 0) for w in weeks)
                persen = (total_hadir / total_minggu) * 100.0
                rekap.set_hadir(nim, persen)
                
        except KeyError:
            print(f"Warning: Baris di attendance.csv tidak valid (kurang student_id/name): {row}")
        except Exception as e:
            print(f"Error memproses baris kehadiran {row.get('student_id')}: {e}")

    # 2. Buat indeks nilai untuk pencarian cepat
    indeks_nilai = {g["student_id"]: g for g in data_nilai}

    # 3. Masukkan nilai ke setiap mahasiswa yang ada di rekap
    for nim in list(rekap._by_nim.keys()):
        nilai_mhs = indeks_nilai.get(nim)
        if nilai_mhs:
            try:
                rekap.set_penilaian(
                    nim,
                    quiz=float(nilai_mhs.get("quiz", 0) or 0),
                    tugas=float(nilai_mhs.get("assignment", 0) or 0),
                    uts=float(nilai_mhs.get("mid", 0) or 0),
                    uas=float(nilai_mhs.get("final", 0) or 0)
                )
            except Exception as e:
                 print(f"Error saat memproses nilai untuk NIM {nim}: {e}")

    print("Info: Data berhasil dimuat.")

# --- Fungsi Helper untuk Tampilan ---

def tampilkan_rekap(rows):
    """Menampilkan data rekap dalam format tabel sederhana di konsol."""
    if not rows:
        print("Tidak ada data untuk ditampilkan.")
        return

    print("\n" + "="*60)
    print(" REKAP KINERJA MAHASISWA")
    print("="*60)
    # Header
    print(f"| {'NIM':<10} | {'Nama':<20} | {'Hadir %':>7} | {'Akhir':>6} | {'Pred':>5} |")
    print("|-" + "-"*10 + "-|-" + "-"*20 + "-|-" + "-"*7 + "-|-" + "-"*6 + "-|-" + "-"*5 + "-|")
    
    # Data
    for r in rows:
        print(f"| {r['nim']:<10} | {r['nama']:<20} | {r['hadir_persen']:>7.2f} | {r['nilai_akhir']:>6.2f} | {r['predikat']:>5} |")
    print("="*60 + "\n")

# --- Fungsi Utama (Menu) ---

def menu():
    """Menjalankan loop menu CLI utama."""
    # Buat satu instance RekapKelas yang akan kita gunakan
    rekap_data = RekapKelas()
    
    while True:
        print("\n=== Student Performance Tracker ===")
        print("1) Muat data dari CSV")
        print("2) Tambah mahasiswa manual")
        print("3) Ubah presensi")
        print("4) Ubah nilai")
        print("5) Lihat rekap")
        print("6) Simpan laporan Markdown (out/report.md)")
        print("7) Keluar")
        
        pilih = input("Pilih (1-7): ").strip()

        try:
            if pilih == "1":
                # Muat data dari CSV
                bootstrap_from_csv(rekap_data)

            elif pilih == "2":
                # Tambah mahasiswa
                nim = input("NIM: ").strip()
                nama = input("Nama: ").strip()
                m = Mahasiswa(nim, nama)
                rekap_data.tambah_mahasiswa(m)

            elif pilih == "3":
                # Set hadir
                nim = input("NIM: ").strip()
                persen = float(input("Hadir % (0-100): ").strip())
                rekap_data.set_hadir(nim, persen)
                print("Info: Kehadiran diperbarui.")

            elif pilih == "4":
                # Set nilai
                nim = input("NIM: ").strip()
                q = float(input("Quiz: ").strip())
                t = float(input("Tugas: ").strip())
                ut = float(input("UTS: ").strip())
                ua = float(input("UAS: ").strip())
                rekap_data.set_penilaian(nim, quiz=q, tugas=t, uts=ut, uas=ua)
                print("Info: Nilai diperbarui.")

            elif pilih == "5":
                # Lihat rekap
                tampilkan_rekap(rekap_data.rekap())

            elif pilih == "6":
                # Simpan laporan Markdown
                print("Membuat laporan...")
                data = rekap_data.rekap()
                if not data:
                    print("Error: Tidak ada data untuk dilaporkan. Muat data dulu.")
                else:
                    laporan_md = build_markdown_report(data)
                    save_text("out/report.md", laporan_md)

            elif pilih == "7":
                # Keluar
                print("Terima kasih. Sampai jumpa!")
                break
                
            else:
                print("Pilihan tidak dikenal. Silakan masukkan angka 1-7.")
                
        except ValueError:
            print("Error: Input tidak valid. Pastikan Anda memasukkan angka yang benar.")
        except KeyError as e:
            print(f"Error: Data tidak ditemukan ({e}).")
        except Exception as e:
            print(f"Terjadi error: {e}")

# --- Titik Masuk Eksekusi ---

if __name__ == "__main__":
    # Pastikan folder 'data' dan 'out' ada
    Path("data").mkdir(exist_ok=True)
    Path("out").mkdir(exist_ok=True)
    
    print("Selamat datang di Aplikasi Perekap Kinerja Mahasiswa.")
    print("Nama: Anindyar Bintang Rahma Esa")
    print("NIM : 230103197")
    
    # Jalankan menu utama
    menu()