#Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
#Örneğin: Türkiye’den IOS kullanıcısı olan 25 yaşındaki bir erkek kullanıcının ortalama ne kadar kazandırabileceği belirlenmek isteniyor.
#Veri seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı tablo tekilleştirilmemiştir.
#Diğer bir ifade ile belirli demografik özelliklere sahip bir kullanıcı birden fazla alışveriş yapmış olabilir.
#Değişkenler
#PRICE – Müşterinin harcama tutarı
#SOURCE – Müşterinin bağlandığı cihaz türü
#SEX – Müşterinin cinsiyeti
#COUNTRY – Müşterinin ülkesi
#AGE – Müşterinin yaşı

#Görev 1: Aşağıdaki Soruları Yanıtlayınız
#Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
import pandas as pd
import numpy as np
import seaborn as sns
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = pd.read_csv("/Users/birsenbayat/Desktop/miuul/PythonProgrammingForDataScience/Dersler/persona.csv")
df

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

#Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique() #2
df["SOURCE"].value_counts()

#Soru 3: Kaç unique PRICE vardır?
df["PRICE"].nunique()
df["PRICE"].value_counts()

#Soru 5: Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts(dropna=False)

#Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY").agg({"PRICE":"sum"}).sort_values("PRICE", ascending=False)

#Soru 7: SOURCE türlerine göre satış sayıları nedir?
df["SOURCE"].value_counts(dropna=False)

#Soru 8: Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY").agg({"PRICE":"mean"})

#Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE":"mean"})

#Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})

#Görev 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).head(50)

#Görev 3: Çıktıyı PRICE’a göre sıralayınız.
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)

#Görev 4: Indekste yer alan isimleri değişken ismine çeviriniz.
agg_df = agg_df.reset_index()

#Görev 5: Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.
agg_df["AGE_CAT"] = pd.cut(df["AGE"], [0, 18, 23, 30, 40, 70], labels=["0_18", "19_23", "24_30", "31_40", "41_70"])


#Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız ve veri setine değişken olarak ekleyiniz.
#Yeni eklenecek değişkenin adı: customers_level_based
pd.set_option("display.float_format", lambda x: "%.2f" % x)
agg_df["customers_level_based"] = agg_df[["COUNTRY", "SOURCE", "SEX", "AGE_CAT"]].agg(lambda x: "_".join(x).upper(), axis=1)
agg_df.head(10)

#!! bu değerleri oluşturduktan sonra bunların tekilleştirilmesi gerekir.
#Örneğin birden fazla şu ifadeden olabilir: USA_ANDROID_MALE_0_18. Bunları groupby'a alıp price ortalamalarını almak gerekmektedir.

new_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})
new_df = new_df.reset_index()

#Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
#Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız.

new_df["SEGMENT"] = pd.qcut(new_df["PRICE"], 4, labels=["D", "C", "B", "A"])
new_df.head(5)

#Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
#33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "TUR_ANDROID_FEMALE_31_40"
new_df[new_df["customers_level_based"] == new_user]

#35 yaşında IOS kullanan bir Fransız kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "FRA_IOS_FEMALE_31_40"
new_df[new_df["customers_level_based"] == new_user]