# Sistem Pendukung Keputusan Pemilihan Supplier Terbaik
## Menggunakan Metode Fuzzy Mamdani dan Sugeno

Proyek ini merupakan implementasi sistem pendukung keputusan untuk memilih supplier terbaik menggunakan dua metode fuzzy logic yang berbeda: Mamdani dan Sugeno.

## Struktur Proyek

```
├── mamdani.py           # Implementasi metode Fuzzy Mamdani
├── sugeno.py            # Implementasi metode Fuzzy Sugeno
├── supplier.xlsx        # Data supplier (input)
├── best_supplier_mamdani.csv  # Hasil output 5 supplier terbaik (Mamdani)
└── best_supplier_sugeno.csv   # Hasil output 5 supplier terbaik (Sugeno)
```

## Penjelasan Komponen

### 1. File Input Data (`supplier.xlsx`)
File Excel yang berisi data supplier dengan kolom:
- `id`: Identifikasi unik supplier
- `kualitas`: Nilai kualitas supplier (skala 0-100)
- `harga`: Harga yang ditawarkan supplier (dalam jutaan rupiah)

### 2. Implementasi Metode Mamdani (`mamdani.py`)

#### Komponen Utama:
1. **Fuzzifikasi**
   - Variabel Kualitas:
     - Very Bad (0-30)
     - Bad (25-55)
     - Good (50-80)
     - Very Good (75-100)
   - Variabel Harga:
     - Cheap (0-4)
     - Affordable (2-8)
     - Expensive (6-∞)

2. **Rule Base**
   - Menggunakan 12 aturan fuzzy
   - Menggunakan operator MIN untuk T-norm
   - Output berupa kategori RENDAH atau TINGGI

3. **Defuzzifikasi**
   - Menggunakan metode Center of Gravity (COG)
   - Range nilai:
     - RENDAH: 10-60
     - TINGGI: 70-100

### 3. Implementasi Metode Sugeno (`sugeno.py`)

#### Komponen Utama:
1. **Fuzzifikasi**
   - Menggunakan variabel linguistik yang sama dengan Mamdani
   - Membership function yang sama untuk input

2. **Rule Base**
   - 12 aturan fuzzy dengan output berupa fungsi linear
   - Contoh fungsi output:
     ```
     IF cheap AND very_bad THEN output = 0.2*kualitas + 0.1*harga + 10
     IF expensive AND very_good THEN output = 0.4*kualitas + 0.2*harga + 40
     ```

3. **Defuzzifikasi**
   - Menggunakan Weighted Average
   - Output berupa nilai numerik langsung

### 4. File Output

1. **`best_supplier_mamdani.csv`**
   - Berisi 5 supplier terbaik berdasarkan metode Mamdani
   - Kolom: id, NK (Nilai Kelayakan), kualitas, harga

2. **`best_supplier_sugeno.csv`**
   - Berisi 5 supplier terbaik berdasarkan metode Sugeno
   - Kolom: id, NK (Nilai Kelayakan), kualitas, harga

## Cara Penggunaan

1. Pastikan data supplier tersedia dalam file `supplier.xlsx`
2. Jalankan metode Mamdani:
   ```
   python mamdani.py
   ```
3. Jalankan metode Sugeno:
   ```
   python sugeno.py
   ```
4. Hasil akan ditampilkan di console dan disimpan dalam file CSV masing-masing

## Perbedaan Utama Kedua Metode

1. **Mamdani**
   - Menggunakan output fuzzy (RENDAH/TINGGI)
   - Proses defuzzifikasi menggunakan COG
   - Output akhir berupa nilai crisp 0-100

2. **Sugeno**
   - Menggunakan output berupa fungsi linear
   - Defuzzifikasi menggunakan weighted average
   - Output berupa nilai numerik langsung

## Kebutuhan Sistem
- Python 3.x
- pandas (untuk membaca file Excel)
- openpyxl (untuk dukungan file Excel) 