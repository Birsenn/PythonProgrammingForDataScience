#############################################
# FEATURE ENGINEERING & DATA PRE-PROCESSING
#############################################

#Eğer veriniz kötü ise, makine öğrenmesi araçlarınız kullanışsız olacaktır -Harward Business Review
#Ham veriden çıkarılabilecek bir çok olası yeni özellik olacağından, sadece iyi veriyle ilgilenmiyoruz, aslında potansiyel veri ile de ilgileniyoruz.

#Appliedmachine learning is basically feature engineering - Andrew Ng

#Özellik mühendisliğ: özellikler üzerinde gerçekleştirilen çalışmalardır. Ham veriden değişken üretmektir.
#Özellik mühendisliği, sadece ML için gerekmez. yapacağımız diğer çalışmalar için de gereklidir.

#%90-%10 bölünmektedir diyebiliriz

#############################################
# 1. Outliers (Aykırı Değerler)
#############################################

#verideki genel eğilimin dışına çıkan değerlerdir.
#özellikle doğrusal problemlerde "aykırı değerler"in etkileri daha fazladır, ağaç yöntemlerde daha azdır.
#buradaki ana nokta, "benim için kabul edilebilir eşik değer nedir?" sorusudur.

#############################################
# Aykırı Değerleri Yakalama
#############################################

#1.sektör bilgisi
#2.standart sapma yaklaşımı
#3.Z-skoru yaklaşımı
#4.boxplot yöntemi


import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
# !pip install missingno
import missingno as msno
from datetime import date
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import LocalOutlierFactor #çok değişkenli outlier yakalama
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

df = load()
df.head()

###################
# Grafik Teknikle Aykırı Değerler
###################

sns.boxplot(x=df["Age"])
plt.show()


###################
# Aykırı Değerler Nasıl Yakalanır?
###################

q1 = df["Age"].quantile(0.25)
q3 = df["Age"].quantile(0.75)
iqr = q3 - q1
up = q3 + 1.5 * iqr
low = q1 - 1.5 * iqr

df[(df["Age"] < low) | (df["Age"] > up)]

df[(df["Age"] < low) | (df["Age"] > up)].index

###################
# Aykırı Değer Var mı Yok mu?
###################

df[(df["Age"] < low) | (df["Age"] > up)].any(axis=None)
df[(df["Age"] < low)].any(axis=None)

#not: burada kritik bir nokta var, low limit eksi değerlerde çıkıyor. değişkenimiz yaş olduğu için yaş eksi olamaz.
#bu nedenle fonksiyon aslında low u dikkate almamış olacak.

# 1. Eşik değer belirledik.
# 2. Aykırılara eriştik.
# 3. Hızlıca aykırı değer var mı yok mu diye sorduk.

###################
# İşlemleri Fonksiyonlaştırmak
###################

def outlier_threshold(dataframe, col_name, q1 = 0.25, q3 = 0.75):
    quartile1 = dataframe[col_name].quantile(q1)
    quartile3 = dataframe[col_name].quantile(q3)
    interquantile_range = quartile3- quartile1
    up_limit = quartile3 + interquantile_range * 1.5
    low_limit = quartile1 - interquantile_range * 1.5
    return low_limit, up_limit

low, up = outlier_threshold(df, "Age")

#artık bu fonksyionu kullanarak istediim değişken için bu işlemi yapabilirim

df[(df["Age"] < low) | (df["Age"] > up)].head()
df[(df["Fare"] < low) | (df["Fare"] > up)].head()

def check_outlier(dataframe, col_name):
    low_limit, up_limit = outlier_threshold(dataframe, col_name)
    if dataframe[(dataframe[col_name] > up_limit) | (dataframe[col_name] < low_limit)].any(axis=None):
        return True
    else:
        return False

check_outlier(df, "Age")
check_outlier(df, "Fare")


###################
# grab_col_names
###################

dff = load_application_train()
dff.head()

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

cat_cols, num_cols, cat_but_car = grab_col_names(df)

num_cols = [col for col in num_cols if col not in "PassengerId"]

for col in num_cols:
    print(col, check_outlier(df, col))


cat_cols, num_cols, cat_but_car = grab_col_names(dff)

num_cols = [col for col in num_cols if col not in "SK_ID_CURR"]

for col in num_cols:
    print(col, check_outlier(dff, col))


###################
# Aykırı Değerlerin Kendilerine Erişmek
###################

def grab_outliers(dataframe, col_name, index=False):
    low, up = outlier_threshold(dataframe, col_name)

    if dataframe[((dataframe[col_name] < low) | (dataframe[col_name] > up))].shape[0] > 10:
        print(dataframe[((dataframe[col_name] < low) | (dataframe[col_name] > up))].head())
    else:
        print(dataframe[((dataframe[col_name] < low) | (dataframe[col_name] > up))])

    if index:
        outlier_index = dataframe[((dataframe[col_name] < low) | (dataframe[col_name] > up))].index
        return outlier_index

grab_outliers(df, "Age")

grab_outliers(df, "Age", True)

age_index = grab_outliers(df, "Age", True)

outlier_thresholds(df, "Age")
check_outlier(df, "Age")
grab_outliers(df, "Age", True)


#############################################
# Aykırı Değer Problemini Çözme
#############################################

###################
# Silme
###################

low, up = outlier_thresholds(df, "Fare")
df.shape

df[~((df["Fare"] < low) | (df["Fare"] > up))].shape

def remove_outlier(dataframe, col_name):
    low_limit, up_limit = outlier_thresholds(dataframe, col_name)
    df_without_outliers = dataframe[~((dataframe[col_name] < low_limit) | (dataframe[col_name] > up_limit))]
    return df_without_outliers


cat_cols, num_cols, cat_but_car = grab_col_names(df)

num_cols = [col for col in num_cols if col not in "PassengerId"]

df.shape

for col in num_cols:
    new_df = remove_outlier(df, col)

df.shape[0] - new_df.shape[0]


###################
# Baskılama Yöntemi (re-assignment with thresholds)
###################

low, up = outlier_thresholds(df, "Fare")

df[((df["Fare"] < low) | (df["Fare"] > up))]["Fare"]

df.loc[((df["Fare"] < low) | (df["Fare"] > up)), "Fare"]

df.loc[(df["Fare"] > up), "Fare"] = up

df.loc[(df["Fare"] < low), "Fare"] = low

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

df = load()
cat_cols, num_cols, cat_but_car = grab_col_names(df)
num_cols = [col for col in num_cols if col not in "PassengerId"]

df.shape

for col in num_cols:
    print(col, check_outlier(df, col))

for col in num_cols:
    replace_with_thresholds(df, col)

for col in num_cols:
    print(col, check_outlier(df, col))


###################
# Recap
###################

df = load()
outlier_thresholds(df, "Age")
check_outlier(df, "Age")
grab_outliers(df, "Age", index=True)

remove_outlier(df, "Age").shape
replace_with_thresholds(df, "Age")
check_outlier(df, "Age")


#############################################
# Çok Değişkenli Aykırı Değer Analizi: Local Outlier Factor
#############################################

# 17, 3

df = sns.load_dataset('diamonds')
df = df.select_dtypes(include=['float64', 'int64'])
df = df.dropna()
df.head()
df.shape
for col in df.columns:
    print(col, check_outlier(df, col))


low, up = outlier_threshold(df, "carat")


df[((df["carat"] < low) | (df["carat"] > up))].shape

low, up = outlier_thresholds(df, "depth")

df[((df["depth"] < low) | (df["depth"] > up))].shape

clf = LocalOutlierFactor(n_neighbors=20)
clf.fit_predict(df)

df_scores = clf.negative_outlier_factor_
df_scores[0:5]
# df_scores = -df_scores
np.sort(df_scores)[0:5]

scores = pd.DataFrame(np.sort(df_scores))
scores.plot(stacked=True, xlim=[0, 50], style='.-')
plt.show()

th = np.sort(df_scores)[3]

df[df_scores < th]

df[df_scores < th].shape


df.describe([0.01, 0.05, 0.75, 0.90, 0.99]).T

df[df_scores < th].index

df[df_scores < th].drop(axis=0, labels=df[df_scores < th].index)

#aykırı değerleri analiz etmek için bazı feature ları birlikte değerlendirmek de gerekebilir.
#mesela tek başına 17 bir aykırı değer değilken, 17 yaşında 3 kere evlenmek aykırıdır gibi.

#LOF yöntemi, çok değişkenli bir aykırı değer gözlemleme yöntemidir.
#gözlemleri, bulundukları konumda yoğunluk tabanlı skorlayarak, buna göre aykırı değer tanımı yapabilmemizi sağlar
#yani bir nokta, komşulularının yoğunluğundan anlamlı bir şekilde düşük ise, bu durumda bu nokta daha seyrek bir
#bölgededir, aykırı değer olabilir diyebiliriz.
#1 den uzaklaştıkça gözlemin outlier olma ihtimali artar

#100 taane değişken nasıl 2 boyutta görselleştirilmiş?

#PCA analizi yöntemi ile yapılır. bu 100 değişkenin taşıdığı bilginin çoğunu taşıyan 2 değişken ile ifade edilir.

#enson!!! baskılama yöntemi kullanabiliriz.
#gözlem sayısı bir miktar fazlaysa, değiştirmek ciddi problemlere sebep olacaktır.
#eğer ağaç yöntemleri ile çalışıyorsak hiç dokunmamalıyız. en fazla çok ucundan dokunmalıyız.(5-95 % methodu gibi)
#doğrusal yöntemleri kullanıyorsak, aykırı değerlerin ciddiyeti devam ediyor olacak. bu aykırı değerleri de doldurmaktan ziyade
#az sayıdaysa silmek tercih edilebilir. ya da ucundan tek değişkneli yaklaşıp baskılamak tercih edilebilir.
