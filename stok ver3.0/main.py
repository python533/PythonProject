import sqlite3
import pandas as pd
from datetime import datetime

def excel_to_database(file_name):
    try:
        df = pd.read_excel(file_name)
        conn = sqlite3.connect('urunler.db')
        cursor = conn.cursor()
        for index, row in df.iterrows():
            try:
                cursor.execute("""INSERT INTO urunler (urun_adi,urun_barkod,urun_stok,kayit_tarihi)
                VALUES(?,?,?,?)""",(row['urun_adi'],['urun_barkod'],['urun_stok'],row['kayit_tarihi']))
                print(f"Urun Eklendi: {row['urun_adi']}")

            except sqlite3.IntegrityError:
                print(f"Hata! {row['urun_barkod']} Bu barkodlu ürün zaten mevcut.Bu Kayıt atlandı!")

        conn.commit()
        conn.close()
        print("Veriler Başarıyl Eklendi.")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

def veritabani_olustur():
    conn = sqlite3.connect('urunler.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS urunliste
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    urun_adi TEXT,
    urun_barkod TEXT,
    urun_stok TEXT,
    kayit_tarihi INTEGER)""")

    conn.commit()
    conn.close()

def guncelle_veritabani_semasi():
    conn = sqlite3.connect('urunler.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE ADD COLUMN guncelleme_tarihi TEXT")
        print("VeriTabanı Şeması Güncellendi:Güncelleme Tarihi Eklendi.")

    except sqlite3.OperationalError:
        print("Veritabanı Bağlantısı Sağlandı.")

        conn.commit()
        conn.close()


def urun_ekle(urun_adi,urun_barkod,urun_stok):
    conn = sqlite3.connect('urunler.db')
    cursor = conn.cursor()
    kayit_tarihi=datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""INSERT INTO urunler (urun_adi,urun_barkod,urun_stok,kayit_tarihi,guncelleme_tarihi) VALUES(?,?,?,?,?)""",
                       (urun_adi,urun_barkod,urun_barkod,urun_stok,kayit_tarihi,None))
        conn.commit()
        print("Ürün Başarıyla Eklendi")
    except sqlite3.Error as e:
        print("Bu Barkod Numarası Zaten Mevcut. Lütfen Farklı Bir Barkod Numarası Kullanın.")
        print(f"Hata Kodu:{e}")
    finally:
        conn.close()

def urunleri_listele(return_data=False):
    conn = sqlite3.connect('urunler.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM urunler")
        urunler = cursor.fetchall()


    except sqlite3.Error as e:
        if return_data:
            return urunler

        else:
            if len(urunler) == 0:
                print("Veritabanında Ürün Bulunamadı!")

    finally:
        conn.close()


def urun_ara(barkod,return_data=False):
    conn = sqlite3.connect('urunler.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urunler WHERE urun_barkod=?",(barkod,))
    urun=cursor.fetchone()
    conn.close()

    if return_data:
        return urun

    else:
        if urun:
            print(f"ID: {urun[0]},Ürün Adı: {urun[1]},Ürün Barkod: {urun[2]},Ürün Stok: {urun[3]},Kayıt Tarihi: {urun[4]}",
                  f"Güncelleme Tarihi: {urun[5] if urun[5] else 'Henüz Güncellenmedi!'}")


        else:
            print("Bu barkoda Sahip ürün bulunamadı!")


def tum_verileri_sil():
    conn = sqlite3.connect('urunler.db')
    cursor = conn.cursor()
    cursor.execute("DELETE * FROM urunler")
    conn.commit()
    conn.close()
    print("Tüm Veriler Silindi!")


def secili_veriyi_sil(barkod):
    conn = sqlite3.connect('urunler.db')
    cursor = conn.cursor()
    cursor.execute("DELETE * FROM urunler WHERE urun_barkod=?",(barkod,))
    if cursor.rowcount > 0:
        print(f"Barkod numarası{barkod}olan kitap silindi.")

    else:
        print("Bu barkoda sahip kitap bulunamad!")
    conn.commit()
    conn.close()


def ürün_düzenle(barkod,yeni_ad,yeni_stok):
    conn = sqlite3.connect('urunler.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urunler WHERE urun_barkod=?",(barkod,))
    urun=cursor.fetchone()

    if urun:
        print(f"Mevcut Bilgiler:Urun Adı:{urun[1]},Stok:{urun[3]}")
        guncelleme_tarihi=datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor.execute("UPDATE urunler SET urun_adi=?,urun_barkod=?,urun_stok=?,kayit_tarihi=?,WHERE urun_barkod=?",
                           (yeni_ad,yeni_stok,guncelleme_tarihi,barkod))
            conn.commit()
            print("Ürün Güncellendi")
            print("Güncelleme Tarihi:",{guncelleme_tarihi})
        
        except sqlite3.Error as e:
            print(f"Güncelleme Sırasında Bir hata meydana geldi:{e}")
            
    else:
        print("Bu barkoda sahip ürün bulunamadı")

    conn.close()

def verileri_excele_aktar(file_name='kitaplar.xlsx'):
    conn = sqlite3.connect('urunler.db')
    df=pd.read_sql_query("SELECT * FROM urunler", conn)
    conn.close()
    df.to_excel(file_name,index=False)
    print(f"Veriler Başarıyla Eklendi: {file_name}dosyasına aktarıldı.")

def ana_menu():
    while True:
        print("\n.1 Ürün Ekle")
        print("\n.2 Ürünleri Listele")
        print("\n.3 Ürün Ara")
        print("\n.4 Tüm Verileri Sil")
        print("\n.5 Seçili Veriyi Sil")
        print("\n.6 Ürün Düzenle")
        print("\n.7 Verileri Excel'e Aktar")
        print("\n.8 Excel'den Verileri İçe Aktar")
        print("\n.9 Çıkış")
        secim=input("Lütfen Bir Seçenek Girin(1-9):")

        if secim=="1":
            ürün_adi=input("Ürün Adı:")
            ürün_barkod=input("Ürün Barkod:")
            ürün_stok=input("Stok")
            #kayit_tarihi=datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            urun_ekle(ürün_adi,ürün_barkod,ürün_stok)

        elif secim=="2":
            urunleri_listele()

        elif secim=="3":
            barkod=input("Aranacak Ürünün Barkod numarasını Girin:")
            urun_ara(barkod)


        elif secim=="4":
            onay=input("Tüm Verileri Silmek İstedğine Emin misin? (E/H):")
            if onay.lower()=="e":
                tum_verileri_sil()

            else:
                print("Veri Silme İşlemi İptal Edildi.")


        elif secim=="5":
            print("Silinecek Verinin Barkodunu Girin:")
            secili_veriyi_sil(barkod)

        elif secim=="6":
            barkod=input("Düzenlecek Ürünün Barkodunu Girin:")
            yeni_ad=input("Yeni Ad:")
            yeni_stok=int(input("Yeni Stok:"))
            ürün_düzenle(barkod,yeni_ad,yeni_stok)


        elif secim=="7":
            verileri_excele_aktar()


        elif secim=="8":
            dosya_adi=input("İçe Aktarılacak Excel dosyasının adını Girin:(örn:Ürünler.xlsx):")
            excel_to_database(dosya_adi)

        elif secim=="9":
            print("Programdan Çıkılıyor!")

        else:
            print("Geçersiz Seçenek. Lütfen Tekrar Deneyin!")

if __name__ == "__main__":
    veritabani_olustur()
    guncelle_veritabani_semasi()
    ana_menu()










































