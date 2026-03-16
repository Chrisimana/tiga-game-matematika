import tkinter as tk
from tkinter import ttk
from games.game_tebak_titik import GameTebakTitik
from games.game_aljabar import GameAljabar
from games.game_parabola import GameParabola

class AplikasiTigaGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 Tiga Game Matematika")
        self.root.geometry("900x830")
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.notebook = ttk.Notebook(self.root)
        
        self.bingkai_titik = ttk.Frame(self.notebook)
        self.bingkai_aljabar = ttk.Frame(self.notebook)
        self.bingkai_parabola = ttk.Frame(self.notebook)
        
        self.notebook.add(self.bingkai_titik, text="🎯 Tebak Titik")
        self.notebook.add(self.bingkai_aljabar, text="🧮 Aljabar")
        self.notebook.add(self.bingkai_parabola, text="🎯 Parabola")
        
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.game_titik = GameTebakTitik(self.bingkai_titik)
        self.game_aljabar = GameAljabar(self.bingkai_aljabar)
        self.game_parabola = GameParabola(self.bingkai_parabola)

    def jalankan(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AplikasiTigaGame()
    app.jalankan()