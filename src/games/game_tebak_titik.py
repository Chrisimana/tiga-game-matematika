import matplotlib.pyplot as plt
import numpy as np
import random
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GameTebakTitik:
    def __init__(self, root):
        self.root = root
        self.ukuran_grafik = 10
        self.jumlah_titik = 5
        self.titik = []
        self.benar = 0
        self.dicoba = 0
        
        self.setup_gui()
        self.setup_game()

    def setup_gui(self):
        self.bingkai_utama = ttk.Frame(self.root)
        self.bingkai_utama.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(self.bingkai_utama, text="🎮 Tebak Koordinat Titik", 
                  font=('Arial', 16, 'bold')).pack(pady=10)
        
        self.fig = Figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self.bingkai_utama)
        self.canvas.get_tk_widget().pack(pady=10)
        
        bingkai_input = ttk.Frame(self.bingkai_utama)
        bingkai_input.pack(pady=10)
        
        ttk.Label(bingkai_input, text="Titik ke-:").grid(row=0, column=0, padx=5)
        self.var_titik = tk.StringVar(value="1")
        ttk.Spinbox(bingkai_input, from_=1, to=5, textvariable=self.var_titik, width=5).grid(row=0, column=1, padx=5)
        
        ttk.Label(bingkai_input, text="X:").grid(row=0, column=2, padx=5)
        self.var_x = tk.StringVar()
        ttk.Entry(bingkai_input, textvariable=self.var_x, width=8).grid(row=0, column=3, padx=5)
        
        ttk.Label(bingkai_input, text="Y:").grid(row=0, column=4, padx=5)
        self.var_y = tk.StringVar()
        ttk.Entry(bingkai_input, textvariable=self.var_y, width=8).grid(row=0, column=5, padx=5)
        
        bingkai_tombol = ttk.Frame(self.bingkai_utama)
        bingkai_tombol.pack(pady=10)
        
        ttk.Button(bingkai_tombol, text="Tebak", command=self.tebak).pack(side='left', padx=5)
        ttk.Button(bingkai_tombol, text="Tingkatkan", command=self.tingkatkan_kesulitan).pack(side='left', padx=5)
        ttk.Button(bingkai_tombol, text="Game Baru", command=self.game_baru).pack(side='left', padx=5)
        
        self.var_skor = tk.StringVar(value="Skor: 0/0 | Akurasi: 0%")
        ttk.Label(self.bingkai_utama, textvariable=self.var_skor, font=('Arial', 10, 'bold')).pack(pady=5)

    def setup_game(self):
        self.titik = [(random.randint(-self.ukuran_grafik+1, self.ukuran_grafik-1),
                      random.randint(-self.ukuran_grafik+1, self.ukuran_grafik-1)) 
                     for _ in range(self.jumlah_titik)]
        self.tampilkan_plot()

    def tampilkan_plot(self):
        self.ax.clear()
        self.ax.set_xlim(-self.ukuran_grafik, self.ukuran_grafik)
        self.ax.set_ylim(-self.ukuran_grafik, self.ukuran_grafik)
        self.ax.grid(True, alpha=0.3)
        
        x_vals = [p[0] for p in self.titik]
        y_vals = [p[1] for p in self.titik]
        self.ax.scatter(x_vals, y_vals, color='red', s=100)
        
        for i, (x, y) in enumerate(self.titik, 1):
            self.ax.text(x, y+0.5, str(i), fontsize=12, ha='center',
                        bbox=dict(boxstyle="round", facecolor='yellow', alpha=0.7))
        
        self.canvas.draw()

    def tebak(self):
        try:
            nomor = int(self.var_titik.get())
            if nomor < 1 or nomor > self.jumlah_titik:
                messagebox.showwarning("Peringatan", "Nomor titik tidak valid!")
                return

            tebakan_x = float(self.var_x.get())
            tebakan_y = float(self.var_y.get())
            
            if not self.var_x.get() or not self.var_y.get():
                messagebox.showwarning("Peringatan", "Masukkan koordinat X dan Y!")
                return

            x_asli, y_asli = self.titik[nomor-1]
            self.dicoba += 1

            if abs(tebakan_x - x_asli) < 0.1 and abs(tebakan_y - y_asli) < 0.1:
                self.benar += 1
                messagebox.showinfo("Benar!", f"✅ ({x_asli}, {y_asli})")
            else:
                messagebox.showinfo("Salah", f"❌ Seharusnya ({x_asli}, {y_asli})")

            self.perbarui_skor()
            self.var_x.set("")
            self.var_y.set("")

        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

    def tingkatkan_kesulitan(self):
        self.ukuran_grafik += 5
        self.jumlah_titik = min(8, self.jumlah_titik + 1)
        self.setup_game()

    def game_baru(self):
        self.benar = 0
        self.dicoba = 0
        self.ukuran_grafik = 10
        self.jumlah_titik = 5
        self.setup_game()
        self.perbarui_skor()

    def perbarui_skor(self):
        akurasi = (self.benar/self.dicoba*100) if self.dicoba > 0 else 0
        self.var_skor.set(f"Skor: {self.benar}/{self.dicoba} | Akurasi: {akurasi:.1f}%")