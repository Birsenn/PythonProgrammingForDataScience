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

df.iloc[0:3] #sıfırdan üçe kadarki elemanlar
df.iloc[0, 0] #sıfırıncı satır ve sıfırıncı sütundaki elemanlar

df.loc[0:3] #isimlendirmenin kendisini seçiyor, yani 3 ü de alıyor
#satır ya da indexlerdeki değerlerin bizzat kendilerine göre seçim işlemi yapmak istersek loc kullanmalıyız

df.iloc[0:3, "age"] #iloc u bu şekilde sütun adını vererek kullanamayız. bu durumda loc kullanmalıyız.
df.loc[0:3, "age"]

col_names = ["age", "embarked", "alive"]
df.loc[0:3, col_names] #birden fazla kolonu da bu şekilde isimlerini ifade ederek seçebiliriz

#######
#Koşullu Seçim (Conditional Selection)
df = sns.load_dataset("titanic")
df[df["age"] > 50].head()
df[df["age"] > 50]["age"].count() #yaşı 50 den büyük olan kaç kişi var
df.loc[df["age"] > 50, ["age", "class"]] #bir koşula bağlı olarak iki özelliği de almak istiyorsak liste tanımlayabiliriz

#eğer birden fazla koşul istiyorsak koşulları parantez içine almalıyız
df_new = df.loc[(df["age"] > 50)
       & (df["sex"] == "male")
       & ((df["embark_town"] == "Cherbourg") | (df["embark_town"] == "Southampton")),
       ["age", "class", "embark_town"]]

df_new["embark_town"].value_counts()

#######
#Toplulaştırma & Gruplama (Aggregation & Grouping)
#toplulaştırma ve gruplama birlikte kullanılırlar
#Toplulaştırma: özet istatistikler veren fonksiyonlardır
#count(), first(), last(), mean(), median(), min(), max(), std(), var(), sum(), pivot_table

df.groupby("sex")["age"].mean() #cinsiyet bazında yaşların ortalamasını aldık
df.groupby("sex").agg({"age": ["mean", "sum"]}) #birden fazla fonksiyon uygulamak istersem "agg" kullanmalıyız
df.groupby("sex").agg({"age": ["mean", "sum"],
                       "embark_town": "count"}) #embark_town u da kırmak istedim fakat bu sistemde cinsiyete göre kırdı.burada  pivot tabloya ihtiyacım var
#o nedenle burada sayısal bir değişken girmek daha mantıklı, deneyelim
df.groupby("sex").agg({"age": ["mean", "sum"],
                       "survived": "mean"}) #burada erkeklerin ve kadınların hayatta kalma yüzdelerini bulmuş olduk

#farklı kategorilere göre kırılım eklemek istediğimde
df.groupby(["sex", "embark_town"]).agg({"age": "mean",
                       "survived": "mean"})

df.groupby(["sex", "embark_town", "class"]).agg({"age": "mean",
                       "survived": "mean",
                         "sex":"count"})

#######
#Pivot Table
#not: pivot table ın default işlemi mean dir.

df.pivot_table("survived", "sex", "embarked") #("values", index, sütunlar)
df.pivot_table("survived", "sex", "embarked", aggfunc="std") #istediğim fonksiyonu da ekleyebilirim
df.pivot_table("survived", "sex", ["embarked", "class"])

#ve yaşa göre de bir analiz yapmak istiyorum ama yaş değişkenlerim integer ve kategorik yapmam lazım
#!!!! cut & qcut fonksiyonu: elimizdeki sayısal değişkenleri kategorik değişkenlere çevirmek için en yaygın kullanılan yöntemdir
#cut: neye göre böleceğimi biliyorsak kullanılır
#qcut: veriyi tanımıyorsam ve çeyrekliklerine göre bölünsün istiyorsak

df["new_age"] = pd.cut(df["age"], [0, 10, 18, 25, 40, 90])
df.pivot_table("survived", ["sex", "new_age"], "embarked")
df.pivot_table("survived", "sex", ["new_age", "class"])

#not: eğer aşağıdaki gibi çıktılar slash ile alt satırda devam etsin istemiyorsak şunu kullanabiliriz:
pd.set_option("display.width", 500)

#######
#Apply & Lambda
#apply: dataframe de satır veya sütunlarda otomatik olarak fonksiyon çalıştırma imkanı sağlar
#lambda: kullan at fonksiyonlardır. tek seferlik fonksiyonları kısa yoldan tanımlamamızı sağlar

df = sns.load_dataset("titanic")

df["age2"] = df["age"]*2
df["age3"] = df["age"]*5

df

for col in df.columns:
    if "age" in col:
        print(col)

for col in df.columns:
    if "age" in col:
        df[col] = df[col]/10

#şimdiye kadar eski yöntemlerle yaptık ve şimdi apply ve lambda ile yapacağız

df[["age", "age2", "age3"]].apply(lambda x: x/10).head()

df.loc[:, df.columns.str.contains("age")].apply(lambda x: x/10).head() #2.yöntemdi. ikisi de kullanılabilir.

#Şimdi dataframe deki değerleri standartlaştıran bir fonksiyon yapacağız

df.loc[:, df.columns.str.contains("age")].apply(lambda x: (x-x.mean()) / x.std()).head() #bu şekilde lambda ile fonksiyonun içine tanımlayabiliriz

def standard_scaler(col_name):
    return (col_name - col_name.mean()) / col_name.std()

df.loc[:, df.columns.str.contains("age")].apply(standard_scaler).head() #bu şekilde direk fonksiyonu apply ın içine yazarak da yapabiliriz

df.loc[:, df.columns.str.contains("age")] = df.loc[:, df.columns.str.contains("age")].apply(standard_scaler).head() #işlemi dataframe e kaydetmek için de yine sol tarafa uygulamak istediğim kolonları yazıyorum
df.head()

#not: apply da axis lerle yine satır veya sütun seçimi yapılabilir

#######
#Birleştirme (join) İşlemleri
m = np.random.randint(1, 30, size=(5, 3))
df1 = pd.DataFrame(m, columns = ["var1", "var2", "var3"])
df2 = df1 + 99

#concat ile birleştirme
pd.concat([df1, df2], ignore_index=True)
#not1: ignore_index ile indexleri düzenli hale getirmiş oluruz
#not2: concat fonksiyonu default olarak alt alta birleştirme yapar, eğer yan yana olsun istiyorsak axis=1 argümanını tanımlamalıyız


#merge ile birleştirme
#daha detaylı birleştirme yapmamızı sağlar

df1 = pd.DataFrame({"employees" : ["john", "dennis", "mark", "maria"],
                    "group" : ["accounting", "engineering", "engineering", "hr"]})

df2 = pd.DataFrame({"employees" : ["john", "dennis", "mark", "maria"],
                    "start_date" : ["2010", "2009", "2014", "2019"]})

pd.merge(df1, df2)
pd.merge(df1, df2, on="employees") #direk de birleştirir fakat on ile birleştirmek istediğimiz sütunu da tanımlayabiliriz
df3 = pd.merge(df1, df2)

df4 = pd.DataFrame({"group" : ["accounting", "engineering", "hr"],
                    "manager" : ["Caner", "Mustafa", "Berkcan"]})

#her çalışanın müdür bilgisine de ulaşmak istiyorum
pd.merge(df3, df4, on="group")
