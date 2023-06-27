#miuul_gezinomi.xlsx: veriyi tanıma
#SaleId : Satış id
#SaleDate : Satış Tarihi
#CheckInDate : Müşterinin otelegirişitarihi
#Price : Satış için ödenen fiyat
#ConceptName: Otel konsept bilgisi
#SaleCityName: Otelin bulunduğu şehir bilgisi
#CInDay:Müşterinin otele giriş günü
#SaleCheckInDayDiff: Check in ile giriş tarihi gün farkı
#Season:Otele giriş tarihindeki sezon bilgisi


#GOREV1
#Soru 1: miuul_gezinomi.xlsx dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
import pandas as pd
import numpy as np
import seaborn as sns
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)

df = pd.read_excel("Dersler/miuul_gezinomi.xlsx")
df.shape

#bunu, veriye genel bir bakış atmamı sağlamak için yazdığım "check_df" fonksiyonuyla yapmak istiyorum
def check_df(dataframe):
    print("############## head ##############")
    print(dataframe.head(10))
    print("############## shape ##############")
    print(dataframe.shape)
    print("############## types ##############")
    print(dataframe.dtypes)
    print("############## info ##############")
    print(dataframe.info())
    print("############## NA ##############")
    print(dataframe.isnull().sum())

check_df(df)

#Soru 2: Kaç unique şehir vardır? Frekansları nedir?
df["SaleCityName"].nunique() #6 tane unique şehir vardır
df["SaleCityName"].value_counts()
df["SaleCityName"].value_counts() / len(df["SaleCityName"])

#Soru 3: Kaç unique Concept vardır?
df["ConceptName"].nunique() #3 unique concept vardır

#Soru 4: Hangi Concept’den kaçar tane satış gerçekleşmiş?
df["ConceptName"].value_counts()

#Soru 5: Şehirlere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("SaleCityName").agg({"Price": "sum"})

#Soru 6: Concept türlerine göre göre ne kadar kazanılmış?
df.groupby("ConceptName")["Price"].agg("sum")

#Soru 7: Şehirlere göre PRICE ortalamaları nedir?
df.groupby("SaleCityName")["Price"].mean()

#Soru8:Conceptlere göre PRICE ortalamaları nedir?
df.groupby("ConceptName")["Price"].agg("mean")

#Soru 9: Şehir-Concept kırılımında PRICE ortalamaları nedir?
df.groupby(["SaleCityName", "ConceptName"]).agg({"Price": "mean"})
#df.groupby(["SaleCityName", "ConceptName"]).agg({"Price": "count"})
#df.groupby(["SaleCityName", "ConceptName"]).agg({"Price": "sum"})

#GOREV2
#SaleCheckInDayDiff değişkenini kategorik bir değişkene çeviriniz.
#SaleCheckInDayDiff değişkeni müşterinin CheckIn tarihinden ne kadar önce satin alımını tamamladığını gösterir.
#Aralıkları ikna edici şekilde oluşturunuz.

df["SaleCheckInDayDiff"].min()
df["new_checkin_diff"] = pd.cut(df["SaleCheckInDayDiff"], [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()],
                                labels = ["Last Minuters", "Potential Planners", "Planners", "Early Bookers"])
df[df["SaleCheckInDayDiff"] == 0]


#GOREV3
#Şehir-Concept-EB Score, Şehir-Concept- Sezon, Şehir-Concept-CInDay kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden inceleyiniz ?
df.groupby
df1 = df.groupby(["SaleCityName", "ConceptName", "new_checkin_diff"]).agg({"Price": ["mean", "count"]})
df1.head(50)

#GOREV4
#City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız.
agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).sort_values("Price", ascending=False)

#GOREV5
#Indekste yer alan isimleri değişken ismine çeviriniz.
#Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çeviriniz.

df1 = df1.reset_index()

#GOREV6
#Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
#Yeni seviye tabanlı satışları tanımlayınız ve veri setine değişken olarak ekleyiniz.
#Yeni eklenecek değişkenin adı: sales_level_based
#Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek sales_level_based değişkenini oluşturmanız gerekmektedir.

df["city"] = [i.upper() for i in df["SaleCityName"]]
df["concept"] = [j.upper() for j in df["ConceptName"]]
df["season"] = [k.upper() for k in df["Seasons"]]
df["sales_level_based"] = df["city"] + "_" + df["concept"] + "_" + df["season"]
df.drop(["city", "concept", "season"], axis=1, inplace=True)

#GOREV7
#Yeni müşterileri (personaları) segmentlere ayırınız.
#Yeni personaları PRICE’a göre 4 segmente ayırınız.
#Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
#Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).

df["SEGMENT"] = pd.qcut(df["Price"], 4, labels=["D", "C", "B", "A"])
agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
agg_df = agg_df.reset_index()
agg_df["city"] = [i.upper() for i in agg_df["SaleCityName"]]
agg_df["concept"] = [j.upper() for j in agg_df["ConceptName"]]
agg_df["season"] = [k.upper() for k in agg_df["Seasons"]]
agg_df["sales_level_based"] = agg_df["city"] + "_" + agg_df["concept"] + "_" + agg_df["season"]
agg_df.drop(["city", "concept", "season"], axis=1, inplace=True)

#Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).
agg_df.groupby("SEGMENT").agg({"Price": ["mean", "max", "sum"]})

#GOREV8
#Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
#Antalya’da herşeydahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama ne kadar gelir kazandırması beklenir?
#Girne’de yarım pansiyon bir otele düşük sezonda giden bir tatilci hangi segmentte yer alacaktır?

agg_df[agg_df["sales_level_based"] == "ANTALYA_HERŞEY DAHIL_HIGH"] #64.920065

#peki müşteri tabanlı kolonu oluşturmasaydım, df ten başka türlü bu bilgiyi nasıl elde ederdim?
df.loc[(df["SaleCityName"] == "Antalya") & (df["ConceptName"] == "Herşey Dahil") & (df["Seasons"] == "High")].agg({"Price": "mean"})

agg_df[agg_df["sales_level_based"] == "GIRNE_YARIM PANSIYON_LOW"] #C segment