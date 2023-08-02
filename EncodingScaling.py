#############################################
# 3. Encoding (Label Encoding, One-Hot Encoding, Rare Encoding)
#############################################

#encoding: değişkenlerin temsil şekillerinin değişitirilmesi
#label encoding: aralarında sıralama olan, ordinallik olan değişkenler için label encoding kullanılabilir.
#çünkü modeller, bu sayısal değerleri büyüklük olarak algılar. yani 0 verileni küçük değer, 1 verileni büyük değer olarak algılar.


#############################################
# Label Encoding & Binary Encoding
#############################################

#2 sınıflı olan label encodinge binary encoding denir. ama aynı şey demektir.

#peki neden encoding kullanıyoruz?
#1- modelin bizden beklentilerinden biri
#2- model tahmin performansını iyileşireceğimiz bazı noktalar olacak, bunu yapabilmek için

#!!! önemli
#bir değişkenin içindeki eşsiz değerleri öğrenmek için nunique yerine neden len(unique) yapmıyorum?
#çünkü unique nan ları da eşsiz değer olarak alacaktır.


import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
#!pip install missingno
import missingno as msno
from datetime import date
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, StandardScaler, RobustScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 500)

def load_application_train():
    data = pd.read_csv("/Users/birsenbayat/Desktop/miuul/PythonProgrammingForDataScience/FeatureEngineering/feature_engineering/feature_engineering/datasets/application_train.csv")
    return data

def load():
    data = pd.read_csv("/Users/birsenbayat/Desktop/miuul/PythonProgrammingForDataScience/FeatureEngineering/feature_engineering/feature_engineering/datasets/titanic.csv")
    return data

def grab_col_names(dataframe, cat_th=10, car_th=20):
    """

    Veri setindeki kategorik, numerik ve kategorik fakat kardinal değişkenlerin isimlerini verir.
    Not: Kategorik değişkenlerin içerisine numerik görünümlü kategorik değişkenler de dahildir.

    Parameters
    ------
        dataframe: dataframe
                Değişken isimleri alınmak istenilen dataframe
        cat_th: int, optional
                numerik fakat kategorik olan değişkenler için sınıf eşik değeri
        car_th: int, optinal
                kategorik fakat kardinal değişkenler için sınıf eşik değeri

    Returns
    ------
        cat_cols: list
                Kategorik değişken listesi
        num_cols: list
                Numerik değişken listesi
        cat_but_car: list
                Kategorik görünümlü kardinal değişken listesi

    Examples
    ------
        import seaborn as sns
        df = sns.load_dataset("iris")
        print(grab_col_names(df))


    Notes
    ------
        cat_cols + num_cols + cat_but_car = toplam değişken sayısı
        num_but_cat cat_cols'un içerisinde.
        Return olan 3 liste toplamı toplam değişken sayısına eşittir: cat_cols + num_cols + cat_but_car = değişken sayısı

    """

    # cat_cols, cat_but_car
    cat_cols = [col for col in dataframe.columns if dataframe[col].dtypes == "O"]
    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and
                   dataframe[col].dtypes != "O"]
    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and
                   dataframe[col].dtypes == "O"]
    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    # num_cols
    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes != "O"]
    num_cols = [col for col in num_cols if col not in num_but_cat]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f'cat_cols: {len(cat_cols)}')
    print(f'num_cols: {len(num_cols)}')
    print(f'cat_but_car: {len(cat_but_car)}')
    print(f'num_but_cat: {len(num_but_cat)}')
    return cat_cols, num_cols, cat_but_car

df = load()
df.head()
df["Sex"].head()

le = LabelEncoder()
le.fit_transform(df["Sex"])[0:5]
le.inverse_transform([0, 1])

def label_encoder(dataframe, binary_col):
    labelencoder = LabelEncoder()
    dataframe[binary_col] = labelencoder.fit_transform(dataframe[binary_col])
    return dataframe

df = load()

binary_cols = [col for col in df.columns if df[col].dtype not in [int, float]
               and df[col].nunique() == 2]

for col in binary_cols:
    label_encoder(df, col)

df.head()

df = load_application_train()
df.shape

binary_cols = [col for col in df.columns if df[col].dtype not in [int, float]
               and df[col].nunique() == 2]

df[binary_cols].head()


for col in binary_cols:
    label_encoder(df, col)

#önemli!!!!!
#veri setini encode ettikten sonra görüyoruz ki, label_encoder nan değerlere de bir şeyler atıyor. 2 değerini gördüğümde bunu anlıyorum
#burada 2 nin nan değerleri ifade ettiğini aklımda tutmam gerekiyor.


df = load()
df["Embarked"].value_counts()
df["Embarked"].nunique()
len(df["Embarked"].unique())

#############################################
# One-Hot Encoding
#############################################

#label encoding ve one hot encoding işlemlerinde sıralamanın öneminden bahsetmiştik.
#ağaç yöntemlerinde dallara ayırma olduğu için burada bu durum da o kadar önemli değildir. doğrusal modellerde önemlidir.
#değişkenlerin aralarında bir sıralama olmadığı durumlarda, model bunu bu şekilde anlamasın diye (mesela 0 daha az etkili gibi)
#one-hot-encoding kullanılmalıdır

df = load()
df.head()
df["Embarked"].value_counts()

pd.get_dummies(df, columns=["Embarked"]).head()

pd.get_dummies(df, columns=["Embarked"], drop_first=True).head()

pd.get_dummies(df, columns=["Embarked"], dummy_na=True).head()

pd.get_dummies(df, columns=["Sex", "Embarked"], drop_first=True).head()

def one_hot_encoder(dataframe, categorical_cols, drop_first=True):
    dataframe = pd.get_dummies(dataframe, columns=categorical_cols, drop_first=drop_first)
    return dataframe

df = load()

# cat_cols, num_cols, cat_but_car = grab_col_names(df)

ohe_cols = [col for col in df.columns if 10 >= df[col].nunique() > 2]


one_hot_encoder(df, ohe_cols).head()

df.head()

#############################################
# Rare Encoding
#############################################

#genelde model geliştirme süreçlerinde karmaşıklık ile değil, basitlik ve genellenebilirlik ile ilgileniyoruz
#herkesi kapsayalım değil, büyük çoğunluğu temsil edelim

#one hot encoding ile oluşturacağım değişkenlerin kalitesinden emin olmak istiyorum

#rare encoding çok sık kullanılan bir yöntem değildir
#çok işe yarar fakat bazı riskleri vardır

#tanım
#bir kategorik değişkenin sınıflarındaki az değerler belirli bir eşik değere göre birleştirilir

#çok kategorik değişkenli bir veri setinde mutlaka rare analyser yapıp, müdahale etmesek bile bunları bilmemiz gerekiyor

# 1. Kategorik değişkenlerin azlık çokluk durumunun analiz edilmesi.
# 2. Rare kategoriler ile bağımlı değişken arasındaki ilişkinin analiz edilmesi.
# 3. Rare encoder yazacağız.

###################
# 1. Kategorik değişkenlerin azlık çokluk durumunun analiz edilmesi.
###################

df = load_application_train()
df.shape #(307511, 122)
df["NAME_EDUCATION_TYPE"].value_counts()

cat_cols, num_cols, cat_but_car = grab_col_names(df)

def cat_summary(dataframe, col_name, plot=False):
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))
    print("##########################################")
    if plot:
        sns.countplot(x=dataframe[col_name], data=dataframe)
        plt.show()


for col in cat_cols:
    cat_summary(df, col)

###################
# 2. Rare kategoriler ile bağımlı değişken arasındaki ilişkinin analiz edilmesi.
###################

df["NAME_INCOME_TYPE"].value_counts()

df.groupby("NAME_INCOME_TYPE")["TARGET"].mean()


def rare_analyser(dataframe, target, cat_cols):
    for col in cat_cols:
        print(col, ":", len(dataframe[col].value_counts()))
        print(pd.DataFrame({"COUNT": dataframe[col].value_counts(),
                            "RATIO": dataframe[col].value_counts() / len(dataframe),
                            "TARGET_MEAN": dataframe.groupby(col)[target].mean()}), end="\n\n\n")

rare_analyser(df, "TARGET", cat_cols)
df.head()

#############################################
# 3. Rare encoder'ın yazılması.
#############################################

def rare_encoder(dataframe, rare_perc):
    temp_df = dataframe.copy()

    rare_columns = [col for col in temp_df.columns if temp_df[col].dtypes == 'O'
                    and (temp_df[col].value_counts() / len(temp_df) < rare_perc).any(axis=None)]

    for var in rare_columns:
        tmp = temp_df[var].value_counts() / len(temp_df)
        rare_labels = tmp[tmp < rare_perc].index
        temp_df[var] = np.where(temp_df[var].isin(rare_labels), 'Rare', temp_df[var])

    return temp_df

new_df = rare_encoder(df, 0.01)

rare_analyser(new_df, "TARGET", cat_cols)

df["OCCUPATION_TYPE"].value_counts()


#############################################
# Feature Scaling (Özellik Ölçeklendirme)
#############################################

#1- modellerin değişkenlere eşit şartlar altında yaklaşmasını sağlamak
#bütün değişkenleri eşit şartlar altında değerlendirebilmek adına ölçeklendirmektir
#2- gradient descent kullanan algoritmaların train sürelerini kısaltmak için kullanılır
#3- KNN, K means gibi uzaklık temelli bazı yöntemler kullanıldığında, ölçekler farklı olduğunda yanlılığa sebep olmaktadır

#!! not: yine ağaç yöntemleri bu durumdan etkilenmez
#ama genel eğilim olarak, ölçeklendirmeyi tercih edebiliriz.

###################
# StandardScaler: Klasik standartlaştırma. Ortalamayı çıkar, standart sapmaya böl. z = (x - u) / s
###################

df = load()
ss = StandardScaler()
df["Age_standard_scaler"] = ss.fit_transform(df[["Age"]])
df.head()


###################
# RobustScaler: Medyanı çıkar iqr'a böl.
###################

#neden???
#bütün gözlem birimlerinden medyanı çıkarıp, IQR a bölsek; hem merkezi eğilimi ve değişimi göz önünde bulundurmuş oluruz hem de daha robust
#aykırı değerlere daha dayanıklı olduğundan dolayı, daha tercih edilebilir olabilir ama kullanımı çok yaygın değildir
#standard scaler yerine kullanılmasını öneriyor

rs = RobustScaler()
df["Age_robuts_scaler"] = rs.fit_transform(df[["Age"]])
df.describe().T

###################
# MinMaxScaler: Verilen 2 değer arasında değişken dönüşümü
###################

# X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
# X_scaled = X_std * (max - min) + min

mms = MinMaxScaler()
df["Age_min_max_scaler"] = mms.fit_transform(df[["Age"]])
df.describe().T

df.head()

age_cols = [col for col in df.columns if "Age" in col]

def num_summary(dataframe, numerical_col, plot=False):
    quantiles = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
    print(dataframe[numerical_col].describe(quantiles).T)

    if plot:
        dataframe[numerical_col].hist(bins=20)
        plt.xlabel(numerical_col)
        plt.title(numerical_col)
        plt.show(block=True)

for col in age_cols:
    num_summary(df, col, plot=True)

###################
# Numeric to Categorical: Sayısal Değişkenleri Kateorik Değişkenlere Çevirme
# Binning
###################

df["Age_qcut"] = pd.qcut(df['Age'], 5)

#############################################
# Feature Extraction (Özellik Çıkarımı)
#############################################

#ham veriden değişken türetmek
#1-yapısal veriden değişken türetmek: veride olan değerleden türetmek
#2-yapısal olmayan verilerden değişken tğretmek: görüntü, ses, yazı gibi...

#############################################
# Binary Features: Flag, Bool, True-False
#############################################

#bu konuda net kabul gören bir literatür yoktur. çünkü özellik çıkarımı işi problemden probleme göre değişebilir.
#var olan değişkenin üzerinden 1-0 şeklinde yeni değişkenler türetmektir
#var olan birden fazla değişkenle birlikte işlem yaparak da en son binary feature üretilebilir (Sibsp + Parch gibi..)

df = load()
df.head()

df["NEW_CABIN_BOOL"] = df["Cabin"].notnull().astype('int')
#burada notnull olan değerleri astype ile integer a çevirmiş oluyoruz.

df.groupby("NEW_CABIN_BOOL").agg({"Survived": "mean"})
#burada gözlemlediğimiz farkı proportion test ile onaylamak istersek:

from statsmodels.stats.proportion import proportions_ztest

test_stat, pvalue = proportions_ztest(count=[df.loc[df["NEW_CABIN_BOOL"] == 1, "Survived"].sum(),
                                             df.loc[df["NEW_CABIN_BOOL"] == 0, "Survived"].sum()],

                                      nobs=[df.loc[df["NEW_CABIN_BOOL"] == 1, "Survived"].shape[0],
                                            df.loc[df["NEW_CABIN_BOOL"] == 0, "Survived"].shape[0]])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#burada hipotez, oranlar arasında anlamlı bir fark yoktur der.
#p < 0.05 olduğu için hipotez reddedilir, vardır diyemeyiz ama bu durumu göz ardı da edemeyiz.
#target değişkeni ne kadar etkileyip etkilemediğini ise model sonuçlarında daha iyi görebilriiz

df.loc[((df['SibSp'] + df['Parch']) > 0), "NEW_IS_ALONE"] = "NO"
df.loc[((df['SibSp'] + df['Parch']) == 0), "NEW_IS_ALONE"] = "YES"

df.groupby("NEW_IS_ALONE").agg({"Survived": "mean"})


test_stat, pvalue = proportions_ztest(count=[df.loc[df["NEW_IS_ALONE"] == "YES", "Survived"].sum(),
                                             df.loc[df["NEW_IS_ALONE"] == "NO", "Survived"].sum()],

                                      nobs=[df.loc[df["NEW_IS_ALONE"] == "YES", "Survived"].shape[0],
                                            df.loc[df["NEW_IS_ALONE"] == "NO", "Survived"].shape[0]])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#############################################
# Text'ler Üzerinden Özellik Türetmek
#############################################

















