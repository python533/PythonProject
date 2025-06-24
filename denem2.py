import random

isim=input("İsminiz Nedir?")

print("İyi Şanslar,",isim)

kelimeler=['şemsiye','bilgisayar','bilim','programlama','python','matematik',
           'oyuncu','kondisyon','su','tahta']

kelime=random.choice(kelimeler)

print("Karakterleri Tahmin Etme")

tahminler=''
donusler=12

while donusler > 0:
    basarısız=0
    for karakter in kelime:
        if karakter in tahminler:
            print(karakter,end=" ")

        else:
            print("_")
            basarısız +=1
        if basarısız == 0:
            print("Kazandın")
            print("Kelime",kelime)
            break

        print()
        tahmin=input("Karakter Tahmin Et?")
        if tahmin in kelimeler:
            tahminler +=tahmin

        if tahmin not in kelime:
            donusler -=1
            print("Yanlış")
            print("Şansın",+donusler,'Daha Fazla Tahmin')

        if donusler == 0:
            print("Kaybettin!")