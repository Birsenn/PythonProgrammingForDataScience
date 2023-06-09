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


#######
#3. Sayısal Değişken Analizi (Analysis of Numerical Variables)

num_cols = [col for col in df.columns if df[col].dtypes in ["int", "float"]]
num_cols = [col for col in num_cols if col not in cat_cols]

def num_summary(dataframe, numerical_col, plot=False):
    quantiles = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
    print(dataframe[numerical_col].describe(quantiles).T)

    if plot:
        dataframe[numerical_col].hist()
        plt.xlabel(numerical_col)
        plt.title(numerical_col)
        plt.show(block=True)


num_summary(df, "age")

for col in num_cols:
    num_summary(df, col, plot=True)

#######
#Değişkenlerin yakalanması ve işlemlerin(Capturing Variables and Generalizing Operations)

#docstring
def grab_col_names(dataframe, cat_th=10, car_th=20):
    """
    Veri setindeki kategorik, numerik ve kategorik fakat kardinal değişkenlerin isimlerini verir.

    Parameters
    ----------
    dataframe: dataframe
        değişken isimleri alınmak istenen dataframe'dir
    cat_th: in, float
        numerik fakat kategorik olan değişkenler için sınıf eşik değeri
    car_th: int, float
        kategorik fakat kardinal değişkenler için sınıf eşik değeri

    Returns
    -------
    cat_cols: list
        kategorik değişken listesi
    num_cols: list
        numerik değişken listesi
    cat_but_car: list
        kategorik görünümlü kardinal değişken listesi

    Notes
    -------
    cat_cols + num_cols + cat_but_car = toplam değişken sayısı
    num_but_cat, cat_cols'un içindedir

    """
    # cat_cols, cat_but_car
    cat_cols = [col for col in df.columns if str(df[col].dtypes) in ["category", "object", "bool"]]
    num_but_cat = [col for col in df.columns if df[col].nunique() < 10 and df[col].dtypes in ["int", "float"]]
    cat_but_car = [col for col in df.columns if
                   df[col].nunique() > 20 and str(df[col].dtypes) in ["category", "object"]]
    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    num_cols = [col for col in df.columns if df[col].dtypes in ["int", "float"]]
    num_cols = [col for col in num_cols if col not in cat_cols]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f"cat_cols: {len(cat_cols)}")
    print(f"num_cols: {len(num_cols)}")
    print(f"cat_but_car: {len(cat_but_car)}")
    print(f"num_but_cat: {len(num_but_cat)}")

    return cat_cols, num_cols, cat_but_car

cat_cols, num_cols, cat_but_car = grab_col_names(df) #çıktılarımı tutmak için tanımlama yapıyorum
help(grab_col_names)

#ekstra: bool için veri dönüşümünü döngülerin içinde yapmaktansa en başta, veriyi analiz ettikten sonra yapıp işlemlere devam etmeliyiz
df = sns.load_dataset("titanic")
df.info()
for col in df.columns:
    if df[col].dtypes == "bool":
        df[col] = df[col].astype(int)

cat_cols, num_cols, cat_but_car = grab_col_names(df)

#kategorikler için analiz
def cat_summary(dataframe, col_name, plot=False):
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))
    print("##################################################")

    if plot:
        sns.countplot(x=dataframe[col_name], data=dataframe)
        plt.show(block=True)

for col in cat_cols:
    cat_summary(df, col, plot=True)

#numerikler için analiz
def num_summary(dataframe, numerical_col, plot=False):
    quantiles = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
    print(dataframe[numerical_col].describe(quantiles).T)

    if plot:
        dataframe[numerical_col].hist()
        plt.xlabel(numerical_col)
        plt.title(numerical_col)
        plt.show(block=True)

for col in num_cols:
    num_summary(df, col, plot=True)


#######
#4. Hedef Değişken Analizi(Analysis of Target Variable)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = sns.load_dataset("titanic")
df.head()

#Hedef değişkenin kategorik değişkenler ile analizi
df.groupby("sex")["survived"].mean()
#bu durumu fonksiyonlaştırmak istersem
def target_sum_with_cat(dataframe, target, categorical_col):
    print(pd.DataFrame({"target_mean": dataframe.groupby(categorical_col)[target].mean()}))

target_sum_with_cat(df, "survived", "sex")

for col in cat_cols:
    target_sum_with_cat(df, "survived", col)
    print("##################################")

#burada aslında ÖLÇEKLENEBİLİRLİK durumunu gerçekleştirmiş olduk. hızlı ve seri bir şekilde target ımızın bütün değişkenler kategorik değişkenler ile ilişkisini inceliyoruz

#Hedef değişkenin sayısal değişkenler ile analizi

df.groupby("survived").agg({"age":"mean"}) #bu defa eksenleri değiştirdik
#bu analizi fonksiyona çevirmek istiyorum
def target_sum_with_num(dataframe, target, numerical_col):
    print(dataframe.groupby(target).agg({numerical_col: "mean"}))

target_sum_with_num(df, "survived", "age")

for col in num_cols:
    target_sum_with_num(df, "survived", col)
    print("#################################")


#######
#5. Korelasyon Analizi(Analysis of Correlation)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = pd.read_csv("/Users/birsenbayat/Desktop/miuul/PythonProgrammingForDataScience/breast_cancer.csv")
df = df.iloc[:, 1:-1]
df.head()

num_cols = [col for col in df.columns if df[col].dtype in [int, float]]

corr = df[num_cols].corr()

#not: birbiriyle yüksek korelasyonlu olan feature lar da datadan çıkarılmalıdır çünkü zaten aynı şey demektir

#heatmap
sns.set(rc={"figure.figsize": (12, 22)})
sns.heatmap(corr, cmap="RdBu")
plt.show()

#Yüksek korelasyonlu değişkenlerin silinmesi

corr_matrix = df.corr().abs()
#öncelikle birden fazla kez gördüğüm korelasyonları dataframe den çıkarmaya çalışcam
upper_triangle_matrix = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

#şimdi korelasyonları yüksek olanları yakalamak istiyorum
drop_list = [col for col in upper_triangle_matrix.columns if any(upper_triangle_matrix[col] > 0.90)]
df.drop(drop_list, axis=1)
df.shape

#şimdi bu yaptığımız işlemi fonksiyon olarak yazmak istiyorum

def high_correlated_cols(dataframe, plot=False, corr_th=0.90):
    corr = dataframe.corr()
    corr_matrix = corr.abs()
    upper_triangle_matrix = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
    drop_list = [col for col in upper_triangle_matrix.columns if any(upper_triangle_matrix[col] > 0.90)]
    if plot:
        import seaborn as sns
        import matplotlib.pyplot as plt
        sns.set(rc={"figure.figsize":(15,15)})
        sns.heatmap(corr, cmap="RdBu")
        plt.show()
    return drop_list

high_correlated_cols(df)
drop_list = high_correlated_cols(df, plot=True)
df.drop(drop_list, axis=1)
high_correlated_cols(df.drop(drop_list, axis=1), plot=True)
