import random

def zar():
    toplam=120
    oyun="Y"

    while oyun=="Y" or oyun=="y":
        print("Toplam Altın'ın var: ",toplam)
        bbet=input("Ne kadarlık Oynamak İstiyorsun? ")
        bet=int(bbet)

        while bet > toplam:
            print("Yeterli Altın'a Sahip Değilsin! Tekrar miktar Belirle?")
            bet=int(bbet)

        print(r"""\_1_/ \_2_/ \_3_/""")
        tahmin=input("Taş Hangi Pot'da ?")
        tahmin=int(tahmin)
        while tahmin > 3:
            print("Tahmin Edilen rakam , üçten büyük!")
            tahmin = input("Taş Hangi Pot'da ?")
            tahmin=int(tahmin)
        zar1=random.randint(1,3)
        print("Taş bu pot'un altında ",zar1)
        if zar1 != tahmin:
            print("Kaybettin!")
            toplam -= bet
        else:
            print("Kazandın!")

        if toplam <=0:
            input("Daha Fazla Hakkın kalmadı,Çıkış Yapmak için enter'a bas")
            break
        oyun=input("Yeniden Oynamak İster misin? (Y/N)")
        oyun=oyun.upper()

        if oyun =="N":
            print("Toplam Altın Miktarı:",toplam,"Altın")
            input("Güle Güle, Çıkış Yapmak İçin Enter'a bas")
zar()





