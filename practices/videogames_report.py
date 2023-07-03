import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = pd.read_csv("/Users/birsenbayat/Desktop/datasets&exercises/videogames_report.csv")


def check_df(dataframe, head=5):
    print("#################### Shape ####################")
    print(dataframe.shape)
    print("#################### Info ####################")
    print(dataframe.info())
    print("#################### Head ####################")
    print(dataframe.head(head))
    print("#################### Tail ####################")
    print(dataframe.tail(head))
    print("#################### NA ####################")
    print(dataframe.isnull().sum())
    print("#################### Quantiles ####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

cat_cols = [col for col in df.columns if str(df[col].dtypes) in ["object", "bool", "category"]]
num_but_cats = [col for col in df.columns if df[col].dtypes in ["int", "float"] and df[col].nunique() < 20]
cat_but_car = [col for col in df.columns if str(df[col].dtypes) in ["object", "bool", "category"] and df[col].nunique() > 600]

cat_cols = [col for col in cat_cols if col not in cat_but_car]

#? mesela bu veri setinde name ler bizim için önemli ama cardinality si yüksek. Ne yapmalıyım?

num_cols = [col for col in df.columns if str(df[col].dtypes) in ["int64", "float64"]]


def cat_summary(dataframe, col_name, plot=False):
    print("################## Ratio ###############")
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": dataframe[col_name].value_counts()/len(dataframe)*100}))

    if True:
        dataframe[col_name].value_counts().plot(kind="bar")
        plt.show()

cat_summary(df, "Genre")

for col in cat_cols:
    cat_summary(df, cat_cols)

def num_summary(dataframe, numerical_col, plot=False):
    quantiles = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
    print(dataframe[numerical_col].describe(quantiles).T)

    if True:
        dataframe[numerical_col].hist()
        plt.xlabel(numerical_col)
        plt.title(numerical_col)
        plt.show(block=True)

for col in num_cols:
    num_summary(df, col)

#şimdi kategorik ve numerik değişkenleri tek seferde analiz edecek bir fonksyion yazacağız
def grab_col_names(dataframe, cat_th=10, car_th=20):
    cat_cols = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["category", "object", "bool"]]
    num_but_cat = [col for col in dataframe.columns if dataframe[col].dtypes in ["float", "int"] and dataframe[col].nunique() < car_th]
    #cat_but_car = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["category", "object", "bool"] and dataframe[col].nunique() > cat_th]

    cat_cols = cat_cols + num_but_cat
    #cat_cols = [col for col in cat_cols if col not in cat_but_car]

    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes in ["float", "int"]]
    num_cols = [col for col in num_cols if col not in num_but_cat]

    print(f"Observation: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f"cat_cols: {len(cat_cols)}")
    print(f"num_cols: {len(num_cols)}")
    #print(f"cat_but_car: {len(cat_but_car)}")
    print(f"num_but_cat: {len(num_but_cat)}")

    return cat_cols, num_cols

cat_cols, num_cols = grab_col_names(df, cat_th=10, car_th=20)

#Hedef değişken analizi
#hedef değişkenin kategorik değişkenler ile analizi
df.groupby("Genre")["Global_Sales"].mean().sort_values(ascending=False)

def target_sum_with_cat(dataframe, col, target_col):
    print(pd.DataFrame({"Target_mean": dataframe.groupby(col)[target_col].mean().sort_values(ascending=False)}))

target_sum_with_cat(df, cat_cols, "Global_Sales")

for col in cat_cols:
    target_sum_with_cat(df, col, "Global_Sales")

#hedef değişkenin sayısal değişkenler ile analizi
df.groupby("Global_Sales").agg({"JP_Sales": "mean"}).sort_values("JP_Sales", ascending=False)

def target_sum_with_num(dataframe, col, target_col):
    print(pd.DataFrame(dataframe.groupby(target_col).agg({col: "mean"})))

target_sum_with_num(df, "JP_Sales", "Global_Sales")

for col in num_cols:
    target_sum_with_num(df, col, "Global_Sales")

#Korelasyon analizi
corr = df[num_cols].corr()

#Heatmap
sns.set(rc={"figure.figsize": (12,22)})
sns.heatmap(corr, cmap="RdBu")
plt.show()

#not:"Global_Sales" ve "NA_Sales" ilişkisi yüksek görünüyor.

#Yüksek korelasyonlu değişkenlerin silinmesi
corr_matrix = df.corr().abs()

#öncelikle yüksek korelasyonlar üzerine işlem yapabilmek için birden fazla gördüğüm değerleri dataframe den çıkarmam gerekiyor
upper_triangle_matrix = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

#şimdi korelasyonları yüksek olanları yakalayabilirim
drop_list = [col for col in upper_triangle_matrix.columns if any(upper_triangle_matrix[col] > 0.9)]

#drop_list ['Global_Sales'] geliyor. Aslında önce bu kolonu silmek istemedim fakat 2 değişkenle de korelasyonu yüksek olduğu için 2 sini silmek
#yerine bunu silmeyi tercih ederim. Ama sadece NA ile yüksek ilişkisi olsaydı onu silmeyi tercih ederdim. Çünkü NA in aslında ne olduğunu bilmiyorum

df.drop(drop_list, axis=1)

#bu işlemi fonksiyon ile yapmak istiyorum
def remove_high_correlated_cols(dataframe, plot=False):
    corr = dataframe.corr()
    corr_matrix = dataframe.corr().abs()
    upper_triangle_matrix = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
    drop_list = [col for col in upper_triangle_matrix.columns if any(upper_triangle_matrix[col] > 0.9)]
    dataframe = dataframe.drop(drop_list, axis=1)
    if plot:
        import seaborn as sns
        import matplotlib.pyplot as plt
        sns.set(rc={"figure.figsize": (12, 22)})
        sns.heatmap(corr, cmap="RdBu")
        plt.show()
    return dataframe

remove_high_correlated_cols(df, plot=True)

#Özet
#Bu çalışmada video games datasetine genel bir bakış attık.
#Kategorik ve numerik değişkenleri tespit ettik, bu değişkenler için özet bir raporlama yaptık (ölçeklenebilir şekilde).
#Değişkenler arasında korelasyonlar nasıl bunu tespit ettik ve yüksek korelasyona sahip olan değişkenlerden birini çıkarmış olduk.
#Devamında null değerleri doldurabiliriz ve kural bazlı sınıflandırma ile bir tahmin yöntemi belirleyebiliriz.
