# Nama: Anindyar Bintang Rahma Esa
# NIM : 230103197
# Proyek: student_performance_tracker

class Penilaian:
    """
    Menyimpan komponen nilai (quiz, tugas, uts, uas) dan menghitung nilai akhir.
    """

    def __init__(self, quiz=0, tugas=0, uts=0, uas=0):
        """
        Membuat instance Penilaian, menginisialisasi semua nilai ke 0
        dan langsung memvalidasinya melalui setter.
        """
        self._quiz = 0.0
        self._tugas = 0.0
        self._uts = 0.0
        self._uas = 0.0
        
        # Gunakan setter saat inisialisasi untuk validasi
        self.quiz = quiz
        self.tugas = tugas
        self.uts = uts
        self.uas = uas

    def _validate(self, nilai):
        """Metode internal untuk validasi nilai 0-100."""
        if not (0 <= nilai <= 100):
            raise ValueError("Nilai harus antara 0 dan 100.")
        return float(nilai)

    # --- Properti dan Setter untuk setiap komponen nilai ---

    @property
    def quiz(self):
        return self._quiz

    @quiz.setter
    def quiz(self, nilai):
        self._quiz = self._validate(nilai)

    @property
    def tugas(self):
        return self._tugas

    @tugas.setter
    def tugas(self, nilai):
        self._tugas = self._validate(nilai)

    @property
    def uts(self):
        return self._uts

    @uts.setter
    def uts(self, nilai):
        self._uts = self._validate(nilai)

    @property
    def uas(self):
        return self._uas

    @uas.setter
    def uas(self, nilai):
        self._uas = self._validate(nilai)

    def nilai_akhir(self):
        """
        Menghitung nilai akhir berdasarkan bobot:
        Quiz (15%), Tugas (25%), UTS (25%), UAS (35%).
        """
        skor = (
            (self.quiz * 0.15) +
            (self.tugas * 0.25) +
            (self.uts * 0.25) +
            (self.uas * 0.35)
        )
        return round(skor, 2)

    def __repr__(self):
        """
        Representasi string dari objek Penilaian.
        """
        return f"<Penilaian Q:{self.quiz} T:{self.tugas} UTS:{self.uts} UAS:{self.uas}>"