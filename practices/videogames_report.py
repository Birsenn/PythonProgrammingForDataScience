import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = pd.read_csv("/Users/birsenbayat/Desktop/datasets&exercises/videogames_report.csv")
df

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
    cat_but_car = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["category", "object", "bool"] and dataframe[col].nunique() > cat_th]

    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes in ["float", "int"]]
    num_cols = [col for col in num_cols if col not in num_but_cat]

    print(f"Observation: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f"cat_cols: {len(cat_cols)}")
    print(f"num_cols: {len(num_cols)}")
    print(f"cat_but_car: {len(cat_but_car)}")
    print(f"num_but_cat: {len(num_but_cat)}")

    return cat_cols, num_cols, cat_but_car

cat_cols, num_cols, cat_but_car = grab_col_names(df, cat_th=10, car_th=20)

#Hedef değişken analizi ile devam edeceğiz.