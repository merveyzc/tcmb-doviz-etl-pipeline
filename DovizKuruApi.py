import requests
import xml.etree.ElementTree as ET
import pandas as pd
from sqlalchemy import create_engine

class DovizKuruETL():
    def __init__(self):
        pass
    
    def doviz_verisi_cek(self):
        url="https://www.tcmb.gov.tr/kurlar/today.xml"
        cevap=requests.get(url)

        agac = ET.fromstring(cevap.content)
        doviz_listesi=[]

        for kur in agac.findall('Currency'):
            kod= kur.get('Kod')
            isim = kur.find('Isim').text
            alis=kur.find('ForexBuying').text
            satis=kur.find('ForexSelling').text

            doviz_listesi.append({
                "Kur_Kodu":kod,
                "Birim_Ismi":isim,
                "Alis_Fiyati":alis,
                "Satis_Fiyati":satis
            })
        df=pd.DataFrame(doviz_listesi)
        df=df.fillna("")
        print(df)
        return df
        

    def sql_veritabanina_yaz(self,df):
        baglanti = 'mssql+pyodbc://@localhost/FintechDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'

        engine= create_engine(baglanti,fast_executemany=True)

        df.to_sql('Gunluk_Doviz_Kurlari', con=engine, if_exists='replace', index=False)
        print("Veriler başarıyla SQL Server'a yazıldı.")
def main():
    proje = DovizKuruETL()

    gelen_veri=proje.doviz_verisi_cek()
    proje.sql_veritabanina_yaz(gelen_veri)

if __name__ == "__main__":
    main()