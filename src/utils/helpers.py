import random

def format_angka(angka, desimal=2):
    #Format angka dengan desimal tertentu
    return f"{angka:.{desimal}f}"

def acak_dalam_rentang(min_val, max_val, desimal=2):
    #Hasilkan angka acak dalam rentang
    return round(random.uniform(min_val, max_val), desimal)

def bersihkan_input(teks):
    #Bersihkan input string
    return teks.strip() if teks else ""