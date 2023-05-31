#Pandas Series

import pandas as pd

s = pd.Series([10, 77, 12, 4, 5])
type(s)
s.index
s.dtype
s.size
s.ndim
s.values
type(s.values)
s.head(3)
s.tail(3)

#######
#Veri Okuma (Reading Data)

df = pd.read_csv("path") #path i direk Pycharm dan soldan da alabiliriz
df.head

#######
#Veriye Hızlı Bakış (Quick Look at Data)

import seaborn as sns

df = sns.load_dataset("titanic")
df.head(5)
df.tail()
df.shape
df.info()
df.columns
df.index
df.describe().T
df.isnull().values.any()
df.isnull().sum() #hangi değişkende kaç tane olduğunu gösterir
df["sex"].head()
df["sex"].value_counts()

#######
#Pandas'ta Seçim İşlemleri (Selection in Pandas) !!!!!!!

df[0:13]
df.drop(0, axis=0).head() #0.indexi sildik. axis=0 satırlardan sil demek, axis=1 sürunlardan sil demek
delete_indexes = [1, 3, 5, 7] #birden fazla index silmek istersek liste halinde verebiliriz
df.drop(delete_indexes, axis=0).head()
#df.drop(delete_indexes, axis=0, inplace=True) **eğer yaptığımız işlemi df te kalıcı hale getirmek istiyorsak, inplace i kullanırız

#Değişkeni Indexe Çevirmek

df["age"].head()
df.age.head()
df.index

df.index = df["age"]
df

df.drop("age", axis=1, inplace=True)
df

#Indexi Değişkene Çevirmek
df["age"] = df.index #1.yol
df

df = df.reset_index() #2.yol / reset index, index kolonunu siler ve onu bir kolon olarak dataframe e ekler

#######
#Değişkenler Üzerine İşlemler

pd.set_option("display.max_columns", None) #üç noktalar yerine bütün kolonları görmek istersek ayar yapmamız gerekir
df = sns.load_dataset("titanic")
df

"age" in df #bir değişkenin veri setinde olup olmadığını görmek istersek

df["age"].head() #tek bir değişkeni böyle seçersek type ı series olur
df[["age"]].head() #tek bir değişkeni hala dataframe olarak kalmasını istiyorsak
df[["age", "alive"]]
col_names = ["age", "alive"]
df[col_names]

df["age2"] = df["age"]**2
df["age3"] = df["age"] / df["age2"]
df
df.drop("age3", axis=1).head()
df.drop(col_names, axis=1).heaD()
df.loc[:, ~df.columns.str.contains("age")].head() #age içeren kolonları silmek istiyorsak. ~ işareti değildir demektir !!!

#######
#loc & iloc
#iloc: integer based selection. yani index bilgisi vererek seçim yapma işlemi.
#loc: label based selection


