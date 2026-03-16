import numpy as np
import random
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GameParabola:
    def __init__(self, root):
        self.root = root
        self.level = 1
        self.tinggi_maks = 10
        self.posisi_tembok = 0
        self.tinggi_tembok = 0
        self.skor = 0
        self.percobaan = 0
        
        self.setup_gui()
        self.level_baru()

    def setup_gui(self):
        self.bingkai_utama = ttk.Frame(self.root)
        self.bingkai_utama.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(self.bingkai_utama, text="🎯 Gerak Parabola", 
                  font=('Arial', 16, 'bold')).pack(pady=10)
        
        self.var_skor = tk.StringVar(value="Skor: 0 | Percobaan: 0 | Akurasi: 0%")
        ttk.Label(self.bingkai_utama, textvariable=self.var_skor).pack(pady=5)
        
        bingkai_level = ttk.Frame(self.bingkai_utama)
        bingkai_level.pack(pady=5)
        ttk.Label(bingkai_level, text="Mode:").pack(side='left')
        self.var_level = tk.IntVar(value=1)
        ttk.Radiobutton(bingkai_level, text="Slider", variable=self.var_level, 
                       value=1, command=self.saat_level_berubah).pack(side='left', padx=10)
        ttk.Radiobutton(bingkai_level, text="Input", variable=self.var_level, 
                       value=2, command=self.saat_level_berubah).pack(side='left', padx=10)
        
        self.bingkai_slider = ttk.Frame(self.bingkai_utama)
        self.slider_a = tk.Scale(self.bingkai_slider, from_=-2, to=2, resolution=0.1,
                                orient='horizontal', label='a:', length=250)
        self.slider_a.pack(pady=2)
        self.slider_b = tk.Scale(self.bingkai_slider, from_=-5, to=5, resolution=0.1,
                                orient='horizontal', label='b:', length=250)
        self.slider_b.pack(pady=2)
        self.slider_c = tk.Scale(self.bingkai_slider, from_=0, to=10, resolution=0.1,
                                orient='horizontal', label='c:', length=250)
        self.slider_c.pack(pady=2)
        
        self.bingkai_input = ttk.Frame(self.bingkai_utama)
        ttk.Label(self.bingkai_input, text="y = ax² + bx + c").pack()
        bingkai_koef = ttk.Frame(self.bingkai_input)
        bingkai_koef.pack(pady=5)
        
        ttk.Label(bingkai_koef, text="a:").pack(side='left')
        self.var_a = tk.StringVar(value="0")
        ttk.Entry(bingkai_koef, textvariable=self.var_a, width=6).pack(side='left', padx=2)
        
        ttk.Label(bingkai_koef, text="b:").pack(side='left')
        self.var_b = tk.StringVar(value="0")
        ttk.Entry(bingkai_koef, textvariable=self.var_b, width=6).pack(side='left', padx=2)
        
        ttk.Label(bingkai_koef, text="c:").pack(side='left')
        self.var_c = tk.StringVar(value="0")
        ttk.Entry(bingkai_koef, textvariable=self.var_c, width=6).pack(side='left', padx=2)
        
        self.slider_a.configure(command=self.perbarui_plot)
        self.slider_b.configure(command=self.perbarui_plot)
        self.slider_c.configure(command=self.perbarui_plot)
        self.var_a.trace('w', lambda *_: self.perbarui_plot())
        self.var_b.trace('w', lambda *_: self.perbarui_plot())
        self.var_c.trace('w', lambda *_: self.perbarui_plot())
        
        self.fig = Figure(figsize=(8, 5))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self.bingkai_utama)
        self.canvas.get_tk_widget().pack(pady=10)
        
        bingkai_tombol = ttk.Frame(self.bingkai_utama)
        bingkai_tombol.pack(pady=5)
        ttk.Button(bingkai_tombol, text="Cek", command=self.cek_solusi).pack(side='left', padx=5)
        ttk.Button(bingkai_tombol, text="Level Baru", command=self.level_baru).pack(side='left', padx=5)
        
        self.var_umpan_balik = tk.StringVar()
        ttk.Label(self.bingkai_utama, textvariable=self.var_umpan_balik, 
                  font=('Arial', 10), wraplength=600).pack(pady=5)
        
        self.bingkai_slider.pack()

    def saat_level_berubah(self):
        if self.var_level.get() == 1:
            self.bingkai_input.pack_forget()
            self.bingkai_slider.pack()
        else:
            self.bingkai_slider.pack_forget()
            self.bingkai_input.pack()
        self.level_baru()

    def level_baru(self):
        self.posisi_tembok = random.uniform(3, 7)
        self.tinggi_tembok = random.uniform(2, 8)
        
        if self.var_level.get() == 1:
            self.slider_a.set(random.uniform(-1, 1))
            self.slider_b.set(random.uniform(-2, 2))
            self.slider_c.set(random.uniform(0, 5))
        else:
            self.var_a.set("0")
            self.var_b.set("0")
            self.var_c.set("0")
        
        self.var_umpan_balik.set(f"🎯 Tembok di x={self.posisi_tembok:.1f}, tinggi={self.tinggi_tembok:.1f}")
        self.perbarui_plot()

    def perbarui_plot(self, event=None):
        self.ax.clear()
        
        try:
            if self.var_level.get() == 1:
                a, b, c = self.slider_a.get(), self.slider_b.get(), self.slider_c.get()
            else:
                a = float(self.var_a.get() or 0)
                b = float(self.var_b.get() or 0)
                c = float(self.var_c.get() or 0)
        except ValueError:
            a, b, c = 0, 0, 0
        
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, self.tinggi_maks)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('Jarak')
        self.ax.set_ylabel('Ketinggian')
        
        self.ax.axvline(x=self.posisi_tembok, color='brown', linewidth=10, alpha=0.5)
        self.ax.axhline(y=self.tinggi_tembok, xmin=self.posisi_tembok/10, 
                       xmax=self.posisi_tembok/10, color='brown', linewidth=2, alpha=0.5)
        self.ax.text(self.posisi_tembok, self.tinggi_tembok+0.5, 
                    f'Tembok\n{self.tinggi_tembok:.1f}m', ha='center')
        
        x = np.linspace(0, 10, 200)
        y = a*x**2 + b*x + c
        
        mask = y >= 0
        if mask.any():
            self.ax.plot(x[mask], y[mask], 'b-', linewidth=2)
            
            y_tembok = a*self.posisi_tembok**2 + b*self.posisi_tembok + c
            if y_tembok >= 0:
                color = 'green' if y_tembok > self.tinggi_tembok else 'red'
                self.ax.plot(self.posisi_tembok, y_tembok, 'o', color=color, markersize=8)
        
        self.canvas.draw()

    def cek_solusi(self):
        try:
            if self.var_level.get() == 1:
                a, b, c = self.slider_a.get(), self.slider_b.get(), self.slider_c.get()
            else:
                a = float(self.var_a.get() or 0)
                b = float(self.var_b.get() or 0)
                c = float(self.var_c.get() or 0)
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")
            return
        
        self.percobaan += 1
        y_tembok = a*self.posisi_tembok**2 + b*self.posisi_tembok + c
        
        if y_tembok > self.tinggi_tembok:
            self.skor += 1
            self.var_umpan_balik.set(f"✅ BERHASIL! y={y_tembok:.1f} > {self.tinggi_tembok:.1f}")
            self.level_baru()
        else:
            selisih = self.tinggi_tembok - y_tembok
            self.var_umpan_balik.set(f"❌ Gagal! y={y_tembok:.1f} < {self.tinggi_tembok:.1f} (kurang {selisih:.1f}m)")
        
        self.perbarui_skor()
        self.perbarui_plot()

    def perbarui_skor(self):
        akurasi = (self.skor/self.percobaan*100) if self.percobaan > 0 else 0
        self.var_skor.set(f"Skor: {self.skor} | Percobaan: {self.percobaan} | Akurasi: {akurasi:.1f}%")