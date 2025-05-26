import pandas as pd
import csv

# membaca data excel dan assign ke variabel
supplier = pd.read_excel('supplier.xlsx')
print(supplier)
panjang_kolom = len(supplier)

# assign id 
supplier_id = supplier['id']
# assign kualitas 
kualitas = supplier['kualitas']
# assign harga
harga = supplier['harga']

# proses fuzzyfication dengan looping banyaknya kolom data
# inisialisasi list kosong untuk menampung nilai setelah deffuzzyfication
def fuzzi_mamdani(supplier_id, kualitas, harga, panjang_kolom):
    # inisialisasi list kosong 
    fuzzy = []
    
    # looping dengan range banyaknya data sebanyak kolom
    for i in range(panjang_kolom):
        # inisialisasi array kosong untuk menampung nilai 
        TK = [0, 0, 0, 0]  # Tingkat Kualitas [very_bad, bad, good, very_good]
        TH = [0, 0, 0]     # Tingkat Harga [cheap, affordable, expensive]
        
        # inisialisasi variabel penilaian = 0
        very_bad = bad = good = very_good = cheap = affordable = expensive = 0
        
        # FUZZIFIKASI UNTUK KUALITAS
        # Membership functions untuk kualitas (0-100)
        if kualitas[i] <= 25:
            very_bad = 1
            TK[0] = very_bad
        elif kualitas[i] > 25 and kualitas[i] < 30:
            very_bad = (30 - kualitas[i]) / (30 - 25)  # BUG FIX: Formula diperbaiki
            bad = (kualitas[i] - 25) / (30 - 25)
            TK[0] = very_bad
            TK[1] = bad
        elif kualitas[i] >= 30 and kualitas[i] <= 50:
            bad = 1
            TK[1] = bad
        elif kualitas[i] > 50 and kualitas[i] < 55:
            bad = (55 - kualitas[i]) / (55 - 50)  # BUG FIX: Formula diperbaiki
            good = (kualitas[i] - 50) / (55 - 50)
            TK[1] = bad
            TK[2] = good
        elif kualitas[i] >= 55 and kualitas[i] <= 75:
            good = 1
            TK[2] = good
        elif kualitas[i] > 75 and kualitas[i] < 80:
            good = (80 - kualitas[i]) / (80 - 75)  # BUG FIX: Formula diperbaiki
            very_good = (kualitas[i] - 75) / (80 - 75)
            TK[2] = good
            TK[3] = very_good
        elif kualitas[i] >= 80:
            very_good = 1
            TK[3] = very_good
            
        # FUZZIFIKASI UNTUK HARGA
        # Membership functions untuk harga (dalam juta rupiah)
        if harga[i] <= 2:
            cheap = 1
            TH[0] = cheap
        elif harga[i] > 2 and harga[i] < 4:
            cheap = (4 - harga[i]) / (4 - 2)      # BUG FIX: Menggunakan harga[i], bukan kualitas[i]
            affordable = (harga[i] - 2) / (4 - 2)  # BUG FIX: Menggunakan harga[i], bukan kualitas[i]
            TH[0] = cheap
            TH[1] = affordable
        elif harga[i] >= 4 and harga[i] <= 6:
            affordable = 1
            TH[1] = affordable
        elif harga[i] > 6 and harga[i] < 8:
            affordable = (8 - harga[i]) / (8 - 6)  # BUG FIX: Menggunakan harga[i], bukan kualitas[i]
            expensive = (harga[i] - 6) / (8 - 6)   # BUG FIX: Menggunakan harga[i], bukan kualitas[i]
            TH[1] = affordable
            TH[2] = expensive
        elif harga[i] >= 8:
            expensive = 1
            TH[2] = expensive 

        # INFERENCE ENGINE - FUZZY RULES (Mamdani)
        # inisialisasi list kosong untuk rekomendasi
        tinggi = []
        rendah = []
        
        # 12 Fuzzy Rules dengan logika MIN untuk T-norm
        # Rules yang menghasilkan rekomendasi RENDAH
        if TH[0] > 0 and TK[0] > 0:  # cheap AND very_bad → rendah
            rendah.append(min(TK[0], TH[0]))
        if TH[1] > 0 and TK[0] > 0:  # affordable AND very_bad → rendah
            rendah.append(min(TK[0], TH[1]))
        if TH[1] > 0 and TK[1] > 0:  # affordable AND bad → rendah
            rendah.append(min(TK[1], TH[1]))
        if TH[2] > 0 and TK[0] > 0:  # expensive AND very_bad → rendah
            rendah.append(min(TK[0], TH[2]))
        if TH[2] > 0 and TK[1] > 0:  # expensive AND bad → rendah
            rendah.append(min(TK[1], TH[2]))
        if TH[2] > 0 and TK[2] > 0:  # expensive AND good → rendah
            rendah.append(min(TK[2], TH[2]))
            
        # Rules yang menghasilkan rekomendasi TINGGI
        if TH[0] > 0 and TK[1] > 0:  # cheap AND bad → tinggi
            tinggi.append(min(TK[1], TH[0]))
        if TH[0] > 0 and TK[2] > 0:  # cheap AND good → tinggi
            tinggi.append(min(TK[2], TH[0]))
        if TH[0] > 0 and TK[3] > 0:  # cheap AND very_good → tinggi
            tinggi.append(min(TK[3], TH[0]))
        if TH[1] > 0 and TK[2] > 0:  # affordable AND good → tinggi
            tinggi.append(min(TK[2], TH[1]))
        if TH[1] > 0 and TK[3] > 0:  # affordable AND very_good → tinggi
            tinggi.append(min(TK[3], TH[1]))
        if TH[2] > 0 and TK[3] > 0:  # expensive AND very_good → tinggi
            tinggi.append(min(TK[3], TH[2]))
        
        # AGREGASI - Menggunakan MAX untuk S-norm
        nilai_tinggi = max(tinggi) if tinggi else 0  # BUG FIX: Handle empty list
        nilai_rendah = max(rendah) if rendah else 0  # BUG FIX: Handle empty list

        # DEFUZZIFIKASI - Center of Gravity (COG) Method
        # Area untuk kategori RENDAH: 10, 20, 30, 40, 50, 60 (6 nilai)
        # Area untuk kategori TINGGI: 70, 80, 90, 100 (4 nilai)
        if (nilai_rendah + nilai_tinggi) > 0:  # BUG FIX: Avoid division by zero
            numerator = (10 + 20 + 30 + 40 + 50 + 60) * nilai_rendah + (70 + 80 + 90 + 100) * nilai_tinggi
            denominator = (6 * nilai_rendah) + (4 * nilai_tinggi)
            y = numerator / denominator
        else:
            y = 50  # Default value jika tidak ada rule yang aktif
            
        # menyimpan data dalam list [id, nilai_kelayakan, kualitas, harga]
        fuzzy.append([supplier_id[i], y, kualitas[i], harga[i]])

    return fuzzy


def main():
    # mengurutkan nilai dari supplier berdasarkan nilai kelayakan dari terbesar ke terkecil
    fuzzy = fuzzi_mamdani(supplier_id, kualitas, harga, panjang_kolom)
    after_sorted = sorted(fuzzy, key=lambda x: x[1], reverse=True)

    # format output dalam bentuk table
    # hitung panjang maksimum dari tiap kolom
    column_width = [max(len(str(x)) for x in column) for column in zip(*after_sorted)]
    
    # output header tabel
    print("id".ljust(column_width[0]), "NK".ljust(column_width[1]), "kualitas".ljust(column_width[2]), "harga".ljust(column_width[3]))
    
    # output pembatas dari header
    print("-" * (column_width[0] + column_width[1] + column_width[2] + 2 + column_width[3] + 9))
    
    # output hasil dalam bentuk tabel
    for inner_list in after_sorted:
        print(str(inner_list[0]).ljust(column_width[0]) + " " + 
              f"{inner_list[1]:.2f}".ljust(column_width[1]) + " " + 
              str(inner_list[2]).ljust(column_width[2]) + "        " + 
              str(inner_list[3]).ljust(column_width[3]))
    
    print('-' * 23)

    # mengambil 5 terbesar dari dalam list
    data0 = after_sorted[:5]

    # format output best supplier dalam tabel
    print("-----Best Supplier (Mamdani Fixed)-----")

    column = [max(len(str(x)) for x in column) for column in zip(*data0)]

    print("id".ljust(column[0]), "NK".ljust(column[1]), "kualitas".ljust(column[2]), "harga".ljust(column[3]))

    print("-" * (column[0] + column[1] + column[2] + 2 + column[3] + 12))

    for inner_list in data0:
        print(str(inner_list[0]).ljust(column[0]) + " " + 
              f"{inner_list[1]:.2f}".ljust(column[1]) + " " + 
              str(inner_list[2]).ljust(column[2]) + "        " + 
              str(inner_list[3]).ljust(column[3]))

    # menyimpan data best supplier dalam bentuk csv
    with open('best_supplier_mamdani.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "NK", "kualitas", "harga"])
        writer.writerows(data0)  # BUG FIX: Langsung tulis data0, tidak perlu wrapper list


if __name__ == "__main__":
    main()