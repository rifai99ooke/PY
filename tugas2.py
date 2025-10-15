print("=== Perhitungan Volume Balok ===\n")

# Input dimensi balok
panjang = float(input("Masukkan panjang balok: "))
lebar = float(input("Masukkan lebar balok: "))
tinggi = float(input("Masukkan tinggi balok: "))

# Rumus volume balok = panjang × lebar × tinggi
volume = panjang * lebar * tinggi

# Menampilkan hasil
print(f"\nPanjang balok: {panjang} cm")
print(f"Lebar balok: {lebar} cm")
print(f"Tinggi balok: {tinggi} cm")
print(f"Volume balok: {volume} cm³")