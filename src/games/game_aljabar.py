import random
import tkinter as tk
from tkinter import ttk, messagebox

class GameAljabar:
    def __init__(self, root):
        self.root = root
        self.tingkat_kesulitan = 1
        self.benar = 0
        self.dicoba = 0
        self.streak = 0
        self.streak_tertinggi = 0
        self.jawaban_sekarang = None
        
        self.setup_gui()
        self.soal_baru()

    def setup_gui(self):
        self.bingkai_utama = ttk.Frame(self.root)
        self.bingkai_utama.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(self.bingkai_utama, text="🧮 Latihan Aljabar", 
                  font=('Arial', 16, 'bold')).pack(pady=10)
        
        self.var_statistik = tk.StringVar(value="Kesulitan: Mudah | Skor: 0/0 | Streak: 0")
        ttk.Label(self.bingkai_utama, textvariable=self.var_statistik, 
                  font=('Arial', 10)).pack(pady=5)
        
        self.var_soal = tk.StringVar(value="Klik 'Soal Baru' untuk memulai!")
        ttk.Label(self.bingkai_utama, textvariable=self.var_soal, 
                  font=('Arial', 14, 'bold'), background='white', 
                  relief='solid', padding=10).pack(pady=20)
        
        bingkai_jawaban = ttk.Frame(self.bingkai_utama)
        bingkai_jawaban.pack(pady=10)
        
        ttk.Label(bingkai_jawaban, text="x =").pack(side='left')
        self.var_jawaban = tk.StringVar()
        entry = ttk.Entry(bingkai_jawaban, textvariable=self.var_jawaban, width=10, font=('Arial', 12))
        entry.pack(side='left', padx=5)
        entry.bind('<Return>', lambda e: self.cek_jawaban())
        
        bingkai_tombol = ttk.Frame(self.bingkai_utama)
        bingkai_tombol.pack(pady=10)
        
        ttk.Button(bingkai_tombol, text="Soal Baru", command=self.soal_baru).pack(side='left', padx=5)
        ttk.Button(bingkai_tombol, text="Cek", command=self.cek_jawaban).pack(side='left', padx=5)
        ttk.Button(bingkai_tombol, text="Kesulitan", command=self.ubah_kesulitan).pack(side='left', padx=5)
        ttk.Button(bingkai_tombol, text="Reset", command=self.reset_game).pack(side='left', padx=5)
        
        self.var_umpan_balik = tk.StringVar()
        ttk.Label(self.bingkai_utama, textvariable=self.var_umpan_balik, 
                  font=('Arial', 11), foreground='blue').pack(pady=10)

    def get_nama_kesulitan(self):
        return {1: "Mudah", 2: "Sedang", 3: "Sulit"}[self.tingkat_kesulitan]

    def soal_baru(self):
        if random.choice([True, False]):
            persamaan, jawaban = self.buat_soal_satu_langkah()
        else:
            persamaan, jawaban = self.buat_soal_dua_langkah()
        
        self.jawaban_sekarang = jawaban
        self.var_soal.set(f"Cari x:\n{persamaan}")
        self.var_jawaban.set("")
        self.var_umpan_balik.set("")

    def buat_soal_satu_langkah(self):
        if self.tingkat_kesulitan == 1:
            a = 1
            b = random.randint(-10, 10)
            c = random.randint(-10, 10)
        elif self.tingkat_kesulitan == 2:
            a = random.choice([1, -1, 2, -2])
            b = random.randint(-20, 20)
            c = random.randint(-20, 20)
        else:
            a = random.randint(-5, 5) or 1
            b = random.randint(-50, 50)
            c = random.randint(-50, 50)

        tanda = "+" if b >= 0 else "-"
        persamaan = f"{'' if a==1 else '-' if a==-1 else a}x {tanda} {abs(b)} = {c}"
        jawaban = round((c - b) / a, 2)
        return persamaan, jawaban

    def buat_soal_dua_langkah(self):
        if self.tingkat_kesulitan == 1:
            a, c = random.randint(1, 5), random.randint(1, 5)
            b, d = random.randint(-10, 10), random.randint(-10, 10)
        elif self.tingkat_kesulitan == 2:
            a, c = random.randint(-5, 5), random.randint(-5, 5)
            b, d = random.randint(-20, 20), random.randint(-20, 20)
        else:
            a, c = random.randint(-10, 10), random.randint(-10, 10)
            b, d = random.randint(-50, 50), random.randint(-50, 50)

        while a == c:
            a = random.randint(-10, 10) or 1

        kiri = f"{'' if a==1 else '-' if a==-1 else a}x"
        kiri += f" + {b}" if b >= 0 else f" - {abs(b)}"
        kanan = f"{'' if c==1 else '-' if c==-1 else c}x"
        kanan += f" + {d}" if d >= 0 else f" - {abs(d)}"
        
        persamaan = f"{kiri} = {kanan}"
        jawaban = round((d - b) / (a - c), 2)
        return persamaan, jawaban

    def cek_jawaban(self):
        if self.jawaban_sekarang is None:
            messagebox.showwarning("Peringatan", "Buat soal dulu!")
            return

        try:
            jawaban_user = float(self.var_jawaban.get())
            self.dicoba += 1

            if abs(jawaban_user - self.jawaban_sekarang) < 0.01:
                self.benar += 1
                self.streak += 1
                self.streak_tertinggi = max(self.streak_tertinggi, self.streak)
                pesan = f"✅ Benar! x = {self.jawaban_sekarang}"
                if self.streak >= 3:
                    pesan += f"\n🔥 Streak {self.streak}!"
            else:
                self.streak = 0
                pesan = f"❌ Salah. x = {self.jawaban_sekarang}"

            self.var_umpan_balik.set(pesan)
            self.perbarui_statistik()
            self.soal_baru()

        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

    def ubah_kesulitan(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Ubah Kesulitan")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Pilih Tingkat Kesulitan:", font=('Arial', 12)).pack(pady=20)
        
        var = tk.IntVar(value=self.tingkat_kesulitan)
        ttk.Radiobutton(dialog, text="Mudah", variable=var, value=1).pack(pady=5)
        ttk.Radiobutton(dialog, text="Sedang", variable=var, value=2).pack(pady=5)
        ttk.Radiobutton(dialog, text="Sulit", variable=var, value=3).pack(pady=5)
        
        def terapkan():
            self.tingkat_kesulitan = var.get()
            self.perbarui_statistik()
            dialog.destroy()
            self.soal_baru()
        
        ttk.Button(dialog, text="Terapkan", command=terapkan).pack(pady=20)

    def reset_game(self):
        self.benar = 0
        self.dicoba = 0
        self.streak = 0
        self.streak_tertinggi = 0
        self.perbarui_statistik()
        self.soal_baru()

    def perbarui_statistik(self):
        akurasi = (self.benar/self.dicoba*100) if self.dicoba > 0 else 0
        self.var_statistik.set(
            f"Kesulitan: {self.get_nama_kesulitan()} | "
            f"Skor: {self.benar}/{self.dicoba} | "
            f"Streak: {self.streak} | Akurasi: {akurasi:.1f}%"
        )