# Nama: Anindyar Bintang Rahma Esa
# NIM : 230103197
# Proyek: student_performance_tracker

from .mahasiswa import Mahasiswa
from .penilaian import Penilaian

class RekapKelas:
    """
    Manajer untuk mengelola banyak objek Mahasiswa dan Penilaian.
    Bertindak sebagai 'service' atau 'controller' utama untuk data kelas.
    """

    def __init__(self):
        """
        Inisialisasi RekapKelas dengan dictionary kosong untuk menyimpan data.
        Struktur: {nim: {'mhs': ObjekMahasiswa, 'nilai': ObjekPenilaian}}
        """
        self._by_nim = {}

    def tambah_mahasiswa(self, mhs):
        """
        Menambahkan objek Mahasiswa baru ke dalam rekap.
        Secara otomatis membuatkan objek Penilaian kosong untuknya.
        
        Args:
            mhs (Mahasiswa): Objek Mahasiswa yang akan ditambahkan.
        """
        if mhs.nim in self._by_nim:
            raise KeyError(f"NIM {mhs.nim} sudah terdaftar.")
        
        self._by_nim[mhs.nim] = {'mhs': mhs, 'nilai': Penilaian()}
        print(f"Info: Mahasiswa {mhs.nama} ({mhs.nim}) ditambahkan.")

    def _get_item(self, nim):
        """Metode helper internal untuk mengambil data mahasiswa berdasarkan NIM."""
        item = self._by_nim.get(nim)
        if not item:
            raise KeyError(f"NIM {nim} tidak ditemukan dalam rekap.")
        return item

    def set_hadir(self, nim, persen):
        """
        Menetapkan persentase kehadiran untuk mahasiswa berdasarkan NIM.
        
        Args:
            nim (str): NIM mahasiswa.
            persen (float/int): Persentase kehadiran (0-100).
        """
        item = self._get_item(nim)
        item['mhs'].hadir_persen = persen

    def set_penilaian(self, nim, quiz=None, tugas=None, uts=None, uas=None):
        """
        Menetapkan nilai untuk mahasiswa berdasarkan NIM.
        Hanya nilai yang tidak 'None' yang akan diperbarui.
        
        Args:
            nim (str): NIM mahasiswa.
            quiz (float/int, optional): Nilai quiz.
            tugas (float/int, optional): Nilai tugas.
            uts (float/int, optional): Nilai UTS.
            uas (float/int, optional): Nilai UAS.
        """
        item = self._get_item(nim)
        p = item['nilai']
        
        if quiz is not None:
            p.quiz = quiz
        if tugas is not None:
            p.tugas = tugas
        if uts is not None:
            p.uts = uts
        if uas is not None:
            p.uas = uas

    def predikat(self, skor):
        """
        Mengonversi skor numerik (0-100) menjadi predikat huruf (A-E).
        
        Args:
            skor (float): Nilai akhir.
            
        Returns:
            str: Predikat (A, B, C, D, atau E).
        """
        if skor >= 85:
            return "A"
        elif skor >= 75:
            return "B"
        elif skor >= 65:
            return "C"
        elif skor >= 50:
            return "D"
        else:
            return "E"

    def rekap(self):
        """
        Menghasilkan rekapitulasi lengkap seluruh mahasiswa dalam bentuk
        list of dictionaries, siap untuk diekspor atau ditampilkan.
        
        Returns:
            list: Sebuah list berisi dictionary untuk setiap mahasiswa.
        """
        rows = []
        for nim, data in self._by_nim.items():
            mhs = data['mhs']
            penilaian = data['nilai']
            
            skor_akhir = penilaian.nilai_akhir()
            predikat_nilai = self.predikat(skor_akhir)
            
            rows.append({
                "nim": mhs.nim,
                "nama": mhs.nama,
                "hadir_persen": mhs.hadir_persen,
                "nilai_akhir": skor_akhir,
                "predikat": predikat_nilai
            })
        return rows