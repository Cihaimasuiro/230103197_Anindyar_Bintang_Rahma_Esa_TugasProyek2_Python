# Nama: Anindyar Bintang Rahma Esa
# NIM : 230103197
# Proyek: student_performance_tracker

class Mahasiswa:
    """
    Merepresentasikan seorang mahasiswa dengan data dasar dan validasi kehadiran.
    """
    
    def __init__(self, nim, nama):
        """
        Membuat instance Mahasiswa baru.

        Args:
            nim (str): Nomor Induk Mahasiswa.
            nama (str): Nama lengkap mahasiswa.
        """
        self.nim = nim
        self.nama = nama
        self._hadir_persen = 0.0  # Atribut 'protected' untuk kehadiran

    @property
    def hadir_persen(self):
        """
        Mendapatkan nilai persentase kehadiran.
        """
        return self._hadir_persen

    @hadir_persen.setter
    def hadir_persen(self, nilai):
        """
        Menetapkan nilai persentase kehadiran dengan validasi 0-100.
        """
        if not (0 <= nilai <= 100):
            raise ValueError("Persentase kehadiran harus antara 0 dan 100.")
        self._hadir_persen = float(nilai)
        
    def info(self):
        """
        Menampilkan profil singkat mahasiswa.
        """
        print(f"NIM  : {self.nim}")
        print(f"Nama : {self.nama}")
        print(f"Hadir: {self.hadir_persen:.2f}%")

    def __repr__(self):
        """
        Representasi string dari objek Mahasiswa.
        """
        return f"<Mahasiswa {self.nim} - {self.nama} (Hadir: {self.hadir_persen:.2f}%)>"