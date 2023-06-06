#Veri Görselleştirme / MATPLOTLIB & SEABORN

#matplotlib, seaborn a göre low level dır. yani bazı konularda daha fazla çaba gerektirir.
#fakat görselleştirme konusunda en temel kütüphane olduğu için diğer kütüphanelerle bir şekilde ilişkilidir ve matplotlib özellikleri kullanılır

#!! HANGİ VERİYİ NASIL GÖRSELLEŞTİRİRİM?

#Kategorik değişken: sütun grafik(barplot). countplot(seaborn) ve barplot(matplotlib) ile yapılır.
#Sayısal değişken: histogram, boxplot. ikisi de dağılım gösterir fakat boxplot aykırı değerleri de gösterir.

#Kategorik Değişken Görselleştirme
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = sns.load_dataset("titanic")
df.head()

df["sex"].value_counts().plot(kind="bar")
plt.show()

#Sayısal Değişken Görselleştirme
plt.hist(df["age"])
plt.show()

plt.boxplot(df["fare"])
plt.show()

#Matplotlib'in Özellikleri
#katmanlı şekilde veri görselleştirme imkanı sağlar

#plot: veriyi görselleşitrmek için kullanılan fonksiyonlardan birisi
x = np.array([1, 8])
y = np.array([0, 150])

plt.plot(x, y)
plt.show()

plt.plot(x, y, "o")
plt.show()

#marker
y = np.array([39, 55, 102, 120])
plt.plot(y, marker = "o")

markers = ["o", "*", ".", ",", "x", "X", "+", "P", "s", "D", "d", "p", "H", "h"]

#line
y = np.array([13, 28, 11, 100])
plt.plot(y, linestyle = "dashdot", color = "r")
plt.show()

#Multiple Lines
x = np.array([23, 18, 31, 10])
plt.plot(x)
plt.plot(y)
plt.show()

#Labels
x = np.array([80, 85, 90, 95])
y = np.array([200, 250, 300, 350])
plt.plot(x, y)
#Başlık
plt.title("Bu ana başlık")
#eksenleri  isimlendirme
plt.xlabel("X ekseni isimlendirme")
plt.ylabel("Y ekseni isimlendirme")
plt.show()

#Subplots
#plot1
x = np.array([80, 85, 90, 95])
y = np.array([200, 250, 300, 350])
plt.subplot(1, 2, 1) #1 satır 2 sütunluk bir grafik oluşturuyorum ve bu birincisi
plt.title("1")
plt.plot(x, y)
plt.show()

#plot2
x = np.random.randint(1, 500, size=(4, 1))
y = np.random.randint(1, 500, size=(4, 1))
plt.subplot(1, 2, 2) #1 satır 2 sütunluk bir grafik oluşturuyorum ve bu ikincisi
plt.title("1")
plt.plot(x, y)
plt.show()

#######
#Seaborn
#Kategorik değişken görselleştirme
df = sns.load_dataset("tips")
sns.countplot(x=df["sex"], data=df)
plt.show()

#Sayısal değişken görselleştirme
sns.boxplot(x=df["total_bill"])
plt.show()

df["total_bill"].hist()
plt.show()