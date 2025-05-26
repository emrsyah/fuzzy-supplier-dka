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
def fuzzi_sugeno(supplier_id, kualitas, harga, panjang_kolom):
    # inisialisasi list kosong 
    fuzzy = []
    
    # looping dengan range banyaknya data sebanyak kolom
    for i in range(panjang_kolom):
        # inisialisasi array kosong untuk menampung nilai 
        TK = [0, 0, 0, 0]  # Tingkat Kualitas
        TH = [0, 0, 0]     # Tingkat Harga
        
        # inisialisasi variabel penilaian = 0
        very_bad = bad = good = very_good = cheap = affordable = expensive = 0
        
        # Fuzzifikasi untuk Kualitas
        if kualitas[i] <= 25:
            very_bad = 1
            TK[0] = very_bad
        elif kualitas[i] > 25 and kualitas[i] < 30:
            bad = -(kualitas[i] - 30)/(30 - 25)
            very_bad = (kualitas[i] - 25)/(30 - 25)
            TK[0] = very_bad
            TK[1] = bad
        elif kualitas[i] >= 30 and kualitas[i] <= 50:
            bad = 1
            TK[1] = bad
        elif kualitas[i] > 50 and kualitas[i] < 55:
            bad = -(kualitas[i] - 55)/(55 - 50)
            good = (kualitas[i] - 50)/(55 - 50)
            TK[1] = bad
            TK[2] = good
        elif kualitas[i] >= 55 and kualitas[i] <= 75:
            good = 1
            TK[2] = good
        elif kualitas[i] > 75 and kualitas[i] < 80:
            good = -(kualitas[i] - 80)/(80 - 75)
            very_good = (kualitas[i] - 75)/(80 - 75)
            TK[2] = good
            TK[3] = very_good
        elif kualitas[i] >= 80:
            very_good = 1
            TK[3] = very_good
            
        # Fuzzifikasi untuk Harga
        if harga[i] <= 2:
            cheap = 1
            TH[0] = cheap
        elif harga[i] > 2 and harga[i] < 4:
            cheap = -(harga[i] - 4)/(4 - 2)  # Perbaikan bug: harga[i] bukan kualitas[i]
            affordable = (harga[i] - 2)/(4 - 2)
            TH[0] = cheap
            TH[1] = affordable
        elif harga[i] >= 4 and harga[i] <= 6:
            affordable = 1
            TH[1] = affordable
        elif harga[i] > 6 and harga[i] < 8:
            affordable = -(harga[i] - 8)/(8 - 6)  # Perbaikan bug: harga[i] bukan kualitas[i]
            expensive = (harga[i] - 6)/(8 - 6)
            TH[1] = affordable
            TH[2] = expensive
        elif harga[i] >= 8:
            expensive = 1
            TH[2] = expensive 

        # SUGENO INFERENCE - Menggunakan fungsi linear untuk output
        rules_and_weights = []
        
        # Rule 1: IF cheap AND very_bad THEN output = 0.2*kualitas + 0.1*harga + 10
        if TH[0] > 0 and TK[0] > 0:
            weight = min(TK[0], TH[0])
            output = 0.2 * kualitas[i] + 0.1 * harga[i] + 10
            rules_and_weights.append((weight, output))
            
        # Rule 2: IF cheap AND bad THEN output = 0.3*kualitas + 0.2*harga + 25
        if TH[0] > 0 and TK[1] > 0:
            weight = min(TK[1], TH[0])
            output = 0.3 * kualitas[i] + 0.2 * harga[i] + 25
            rules_and_weights.append((weight, output))
            
        # Rule 3: IF cheap AND good THEN output = 0.5*kualitas + 0.1*harga + 40
        if TH[0] > 0 and TK[2] > 0:
            weight = min(TK[2], TH[0])
            output = 0.5 * kualitas[i] + 0.1 * harga[i] + 40
            rules_and_weights.append((weight, output))
            
        # Rule 4: IF cheap AND very_good THEN output = 0.6*kualitas + 0.05*harga + 50
        if TH[0] > 0 and TK[3] > 0:
            weight = min(TK[3], TH[0])
            output = 0.6 * kualitas[i] + 0.05 * harga[i] + 50
            rules_and_weights.append((weight, output))
            
        # Rule 5: IF affordable AND very_bad THEN output = 0.15*kualitas + 0.2*harga + 15
        if TH[1] > 0 and TK[0] > 0:
            weight = min(TK[0], TH[1])
            output = 0.15 * kualitas[i] + 0.2 * harga[i] + 15
            rules_and_weights.append((weight, output))
            
        # Rule 6: IF affordable AND bad THEN output = 0.25*kualitas + 0.3*harga + 20
        if TH[1] > 0 and TK[1] > 0:
            weight = min(TK[1], TH[1])
            output = 0.25 * kualitas[i] + 0.3 * harga[i] + 20
            rules_and_weights.append((weight, output))
            
        # Rule 7: IF affordable AND good THEN output = 0.4*kualitas + 0.2*harga + 35
        if TH[1] > 0 and TK[2] > 0:
            weight = min(TK[2], TH[1])
            output = 0.4 * kualitas[i] + 0.2 * harga[i] + 35
            rules_and_weights.append((weight, output))
            
        # Rule 8: IF affordable AND very_good THEN output = 0.5*kualitas + 0.1*harga + 45
        if TH[1] > 0 and TK[3] > 0:
            weight = min(TK[3], TH[1])
            output = 0.5 * kualitas[i] + 0.1 * harga[i] + 45
            rules_and_weights.append((weight, output))
            
        # Rule 9: IF expensive AND very_bad THEN output = 0.1*kualitas + 0.4*harga + 5
        if TH[2] > 0 and TK[0] > 0:
            weight = min(TK[0], TH[2])
            output = 0.1 * kualitas[i] + 0.4 * harga[i] + 5
            rules_and_weights.append((weight, output))
            
        # Rule 10: IF expensive AND bad THEN output = 0.2*kualitas + 0.5*harga + 10
        if TH[2] > 0 and TK[1] > 0:
            weight = min(TK[1], TH[2])
            output = 0.2 * kualitas[i] + 0.5 * harga[i] + 10
            rules_and_weights.append((weight, output))
            
        # Rule 11: IF expensive AND good THEN output = 0.3*kualitas + 0.3*harga + 25
        if TH[2] > 0 and TK[2] > 0:
            weight = min(TK[2], TH[2])
            output = 0.3 * kualitas[i] + 0.3 * harga[i] + 25
            rules_and_weights.append((weight, output))
            
        # Rule 12: IF expensive AND very_good THEN output = 0.4*kualitas + 0.2*harga + 40
        if TH[2] > 0 and TK[3] > 0:
            weight = min(TK[3], TH[2])
            output = 0.4 * kualitas[i] + 0.2 * harga[i] + 40
            rules_and_weights.append((weight, output))
        
        # SUGENO DEFUZZIFICATION - Weighted Average
        if rules_and_weights:
            total_weighted_output = sum(weight * output for weight, output in rules_and_weights)
            total_weights = sum(weight for weight, output in rules_and_weights)
            
            if total_weights > 0:
                final_output = total_weighted_output / total_weights
            else:
                final_output = 0
        else:
            final_output = 0
            
        # menyimpan data dalam list
        fuzzy.append([supplier_id[i], final_output, kualitas[i], harga[i]])

    return fuzzy


def main():
    # mengurutkan nilai dari supplier berdasarkan nilai kelayakan dari terbesar ke terkecil
    fuzzy = fuzzi_sugeno(supplier_id, kualitas, harga, panjang_kolom)
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
    print("-----Best Supplier (Sugeno Method)-----")

    column = [max(len(str(x)) for x in column) for column in zip(*data0)]

    print("id".ljust(column[0]), "NK".ljust(column[1]), "kualitas".ljust(column[2]), "harga".ljust(column[3]))

    print("-" * (column[0] + column[1] + column[2] + 2 + column[3] + 12))

    for inner_list in data0:
        print(str(inner_list[0]).ljust(column[0]) + " " + 
              f"{inner_list[1]:.2f}".ljust(column[1]) + " " + 
              str(inner_list[2]).ljust(column[2]) + "        " + 
              str(inner_list[3]).ljust(column[3]))

    # menyimpan data best supplier dalam bentuk csv
    data = [after_sorted[:5]]
    with open('best_supplier_sugeno.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "NK", "kualitas", "harga"])
        for inner_list in data:
            writer.writerows(inner_list)


if __name__ == "__main__":
    main()