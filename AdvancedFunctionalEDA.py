#GELİŞMİŞ FONKSİYONEL KEŞİFÇİ VERİ ANALİZİ(ADVANCED FUNCTIONAL EDA)
#Amaç: hızlı bir şekilde veri ile ilgili iç görüler elde edebilmek

#1. Genel Resim
#2. Kategorik Değişken Analizi (Analysis of Categorical Variables)
#3. Sayısal Değişken Analizi (Analysis of Numerical Variables)
#4. Hedef Değişken Analizi (Analysis of Target Variables)
#5. Korelasyon Analizi (Analysis of Correlation)

#1. Genel Resim
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = sns.load_dataset("titanic")
df.head()

def check_df(dataframe, head=5):
    print("#################### Shape ####################")
    print(dataframe.shape)
    print("#################### Types ####################")
    print(dataframe.dtypes)
    print("#################### Head ####################")
    print(dataframe.head(head))
    print("#################### Tail ####################")
    print(dataframe.tail(head))
    print("#################### NA ####################")
    print(dataframe.isnull().sum())
    print("#################### Quantiles ####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

df = sns.load_dataset("flights")
check_df(df)

#######
#2. Kategorik Değişken Analizi (Analysis of Categorical Variables)
#fonksiyonel şekilde, genellenebilirlik kaygısıyla değişken tiplerini yakalamayı ve bunların özelinde analiz yapacak bir fonksiyon yazma işlemini gerçekleştireceğiz
df = sns.load_dataset("titanic")

df["embarked"].value_counts()
df["sex"].unique() #unique olan değişkenleri verir
df["sex"].nunique() #unique olan değişkenlerin sayısını verir

#1.bildiğimiz anlamda kategorik olan değişkenleri yakalıyoruz
cat_cols = [col for col in df.columns if str(df[col].dtypes) in ["category", "object", "bool"]]
cat_cols

#2.burada ise nicel gibi görünen ama aslında olmayan değişkenleri de yakalıyoruz
num_but_cat = [col for col in df.columns if df[col].nunique() < 10 and df[col].dtypes in ["int", "float"] ]

#3.kategorik olan fakat sınıf sayısı çok fazla olan(high cardinality) kolonları bulma
#high cardinality: ölçülemeyecek kadar fazla sınıfı vardır anlamına gelir

cat_but_car = [col for col in df.columns if df[col].nunique() > 20 and str(df[col].dtypes) in ["category", "object"]]

cat_cols = cat_cols + num_but_cat #kategorik olanların hepsini topladık
cat_cols = [col for col in cat_cols if col not in cat_but_car] #fakat bunları high cardinality değilse dahil et dedik

df[cat_cols].nunique()

#şimdi her değişkenin value counts larını yüzde olarak yazacak bir fonksiyon yazacağız
def cat_summary1(dataframe, col_name):
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))
    print("##################################################")

cat_summary(df, "sex")

for col in cat_cols:
    cat_summary(df, col)

#Bölüm2: şimdi bir de grafik çizdirmek istiyorum

def cat_summary(dataframe, col_name, plot=False):
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))
    print("##################################################")

    if plot:
        sns.countplot(x=dataframe[col_name], data=dataframe)
        plt.show(block=True)

cat_summary(df, "sex", plot=True)

for col in cat_cols:
    cat_summary(df, col, plot=True) #fakat burada "bool" type ının grafiğini çizemediği için biraz değiştirmemiz gerekiyor aşağıdaki gibi bir çözüm buluyorum,

for col in cat_cols:
    if df[col].dtypes == "bool":
        cat_summary1(df, col)
    else:
        cat_summary(df, col, plot=True)

#bu değişkeni es geçmektense, tipini değiştirip de fonksiyona dahil edebilirim
for col in cat_cols:
    if df[col].dtypes == "bool":
        df[col] = df[col].astype(int)
        cat_summary(df, col, plot=True)
    else:
        cat_summary(df, col, plot=True)

#şimdi bir de bu durumu fonksiyonumuzun içine tanımlayıp yapacağız. fakat kod karışıklığına sebep olacağı için kesinlikle tercih edilen bir yöntem değildir
def cat_summary(dataframe, col_name, plot=False):
    if dataframe[col_name].dtypes == "bool":
        dataframe[col_name] = dataframe[col_name].astype(int)

        print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                            "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))
        print("####################################")

        if plot: #burası, "eğer plot özelliği açıksa" demek
            sns.countplot(x=dataframe[col_name], data=dataframe)
            plt.show(block=True)

    else:
        print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                            "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))
        print("####################################")
        if plot:
            sns.countplot(x=dataframe[col_name], data=dataframe)
            plt.show(block=True) #döngü içinde birden fazla grafik çizileceği için karışıklığı engellemek için block=True diyoruz

cat_summary(df, "adult_male", plot=True) #fonksiyon içinde halledebildik fakat kod epey bir karıştı. bu nedenle ilk yöntem tercih edilmeli