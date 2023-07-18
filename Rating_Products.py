##########################################
#Ölçüm Problemleri (Measurement Problems)
##########################################

#müşteri bir ürünü alırken bakacağı bir çok parametre olabilir. fakat son yıllarda "social proof" kavramı bir kullanıcının satınalmasını en çok
#etkileyen kavramdır. toplumun ürüne ne tepki verdiğini anlamaya çalışıyor.

#The Wisdom of Crowds (Kalabalıkların Bilgeliği)

#hassas olan nokta: kullanıcının social proof touch pointlerini, en olması gerektiği objektiflikte, doğru şekilde vermek gerektiğidir.
#bu durum, ürünlere yapılan yorumların sıralanmasına ve ürün puanlarının hesaplamalarına denk gelmektedir

# *Ürün puanlarının hesaplanması
# *ürünlerin sıralanması
# *ürün detay sayfalarındaki kullanıcı yorumlarının sıralanması
# *sayfa, süre, etkileşim alanlarının tasarımları
# *özellik denemeleri
# *olası aksiyon ve reaksiyonların test edilmesi

#Nasıl yapacağız?
#1-Rating products
#2-Sorting products
#3-Sorting reviews
#4-AB Testing
#5-Dynamic pricing


###################################################
# Rating Products
###################################################

# - Average
# - Time-Based Weighted Average
# - User-Based Weighted Average
# - Weighted Rating


############################################
# Uygulama: Kullanıcı ve Zaman Ağırlıklı Kurs Puanı Hesaplama
############################################

#bir ürüne verilen puanlar üzerinden çeşitli değrlendirmeler yaparak, en doğru puanın nasıl hesaplanacağını göreceğiz
import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_csv("/Users/birsenbayat/Desktop/miuul/PythonProgrammingForDataScience/Measurement_Problems/measurement_problems/datasets/course_reviews.csv")
df.head()

df["Rating"].value_counts()
df["Questions Asked"].value_counts()

df.groupby("Questions Asked").agg({"Questions Asked": "count",
                                   "Rating": "mean"}).sort_values(by="Rating", ascending=False)
####################
# Average
####################

# Ortalama Puan
df["Rating"].mean()
#not: direk rating in ortalamasına bakarsak, trendi kaçırabiliriz. mesela son zamanlarda çıkabilecek negatif veya pozitif trendler kaçabilir.

####################
# Time-Based Weighted Average
####################
# Puan Zamanlarına Göre Ağırlıklı Ortalama

df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df.dtypes

df["Timestamp"].max()

current_date = pd.to_datetime('2021-02-10 0:0:0')

df["days"] = (current_date - df["Timestamp"]).dt.days
df.head()


df.loc[df["days"] <= 30, "Rating"].mean()

df.loc[(df["days"] > 30) & (df["days"] <= 90), "Rating"].mean()

df.loc[(df["days"] > 90) & (df["days"] <= 180), "Rating"].mean()

df.loc[(df["days"] > 180), "Rating"].mean()

#ağırlıkları değiştirerek kullanabileceğimiz fonksiyon
def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[dataframe["days"] <= 30, "Rating"].mean() * w1/100 + \
        dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "Rating"].mean() * w2/100 + \
        dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "Rating"].mean() * w3 / 100 + \
        dataframe.loc[dataframe["days"] > 180, "Rating"].mean() * w4 / 100

time_based_weighted_average(df, 30, 26, 22, 22)

#not: virgülden sonraki rakamlardan kazanılan miktarlar çok farkettirir. dikkat etmemiz lazım. sıralama 4. basamaktan sonra değişebilir.

####################
# User-Based Weighted Average
####################

#bütün kullanıcıların verdikleri puanlar aynı şekilde mi dikkate alınmalı?
#kursu izleme oranlarına göre mi puanlar dikkate alınmalı?

df.groupby("Progress").agg({"Rating":"mean"})

def user_based_weighted_average(dataframe, w1=22, w2=24, w3=26, w4=28):
    return dataframe.loc[dataframe["Progress"] <= 10, "Rating"].mean() * w1/100 + \
        dataframe.loc[(dataframe["Progress"] > 10) & (dataframe["Progress"] <= 45), "Rating"].mean() * w2 / 100 + \
        dataframe.loc[(dataframe["Progress"] > 45) & (dataframe["Progress"] <= 75), "Rating"].mean() * w3 / 100 + \
        dataframe.loc[(dataframe["Progress"] > 75), "Rating"].mean() * w4 / 100

user_based_weighted_average(df, 20, 24, 26, 30)


####################
# Weighted Rating
####################

def course_weighted_rating(dataframe, time_w=50, user_w=50):
    return time_based_weighted_average(dataframe) * time_w/100 + user_based_weighted_average(dataframe) * user_w/100

course_weighted_rating(df)
course_weighted_rating(df, time_w=40, user_w=60)