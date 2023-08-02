#############################################
# Missing Values (Eksik Değerler)
#############################################

#1- Silme
#2- Değer atama yöntemleri
#3- Tahmine dayalı yöntemler (ML veya istatistiki yöntemler ile atama yapılması)

#değer atama yöntemleri, hem çekici hem tehlikelidir.
#eksik veri ile çalışılırken göz önünde bulundurulması gereken önemli konulardan biri: eksik verinin rassallığı

#yani eksik değerlerin rastgele ortaya çıkıp çıkmadığı konusudur. restgele ortaya çıktıysa silinebilir.
#eğer eksiklikler, değişkenlerle ilişki olarak ortyaa çıkan yapısal problemler ile meydana gelmişse, bu durumda silme işlemi
#ciddi yanlılıklara sebep olabilecektir

#junior larla seniorların ayrıldığı nokta:
#rastgele oluşmayan ama başka bir değişkene bağlı olarak null olan değişkenler için ne yapmalıyım?
#yapacağımız doldurma işlemlerinin bazı problemlere sebep olabileceğini düşünmek gerekir, adım atarken 2 kere düşünmek gerekir
#bu yapısallığın nerden kaynaklandığını bulup, onun üzerine gitmek güzel bir çözüm olacaktır

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



#############################################
# Eksik Değerlerin Yakalanması
#############################################

df = load()
df.head()
df.info()
df["Embarked"].nunique()

# eksik gozlem var mı yok mu sorgusu
df.isnull().values.any()

# degiskenlerdeki eksik deger sayisi
df.isnull().sum()

# degiskenlerdeki tam deger sayisi
df.notnull().sum()

# veri setindeki toplam eksik deger sayisi
df.isnull().sum().sum()

# en az bir tane eksik degere sahip olan gözlem birimleri
df[df.isnull().any(axis=1)]

# tam olan gözlem birimleri
df[df.notnull().all(axis=1)]

# Azalan şekilde sıralamak
df.isnull().sum().sort_values(ascending=False)

(df.isnull().sum() / df.shape[0] * 100).sort_values(ascending=False)

na_cols = [col for col in df.columns if df[col].isnull().sum() > 0]


def missing_values_table(dataframe, na_name=False):
    na_columns = [col for col in dataframe.columns if dataframe[col].isnull().sum() > 0]

    n_miss = dataframe[na_columns].isnull().sum().sort_values(ascending=False)
    ratio = (dataframe[na_columns].isnull().sum() / dataframe.shape[0] * 100).sort_values(ascending=False)
    missing_df = pd.concat([n_miss, np.round(ratio, 2)], axis=1, keys=['n_miss', 'ratio'])
    print(missing_df, end="\n")

    if na_name:
        return na_columns


missing_values_table(df)

missing_values_table(df, True)


#############################################
# Eksik Değer Problemini Çözme
#############################################

missing_values_table(df)

###################
# Çözüm 1: Hızlıca silmek
###################
df.dropna().shape

###################
# Çözüm 2: Basit Atama Yöntemleri ile Doldurmak
###################

df["Age"].fillna(df["Age"].mean()).isnull().sum()
df["Age"].fillna(df["Age"].median()).isnull().sum()
df["Age"].fillna(0).isnull().sum()

# df.apply(lambda x: x.fillna(x.mean()), axis=0)

df.apply(lambda x: x.fillna(x.mean()) if x.dtype != "O" else x, axis=0).head()

dff = df.apply(lambda x: x.fillna(x.mean()) if x.dtype != "O" else x, axis=0)

dff.isnull().sum().sort_values(ascending=False)

df["Embarked"].fillna(df["Embarked"].mode()[0]).isnull().sum()

df["Embarked"].fillna("missing")

df.apply(lambda x: x.fillna(x.mode()[0]) if (x.dtype == "O" and len(x.unique()) <= 10) else x, axis=0).isnull().sum()

###################
# Kategorik Değişken Kırılımında Değer Atama
###################

#buradaki amaç, bazı kategorik değişkenlerin yönlendirmesine göre eksik değerleri doldurmak. mesela yaş değişkenindeki boş değerleri
#doldururken, kadınlar ve erkeklerin yaş ortalamalarına göre doldurmak daha doğru olacaktır.

df.groupby("Sex")["Age"].mean()

df["Age"].fillna(df.groupby("Sex")["Age"].transform("mean")).isnull().sum()

df.groupby("Sex")["Age"].mean()["female"]

df.loc[(df["Age"].isnull()) & (df["Sex"] == "female"), "Age"] = df.groupby("Sex")["Age"].mean()["female"]
df.loc[(df["Age"].isnull()) & (df["Sex"] == "male"), "Age"] = df.groupby("Sex")["Age"].mean()["male"]

df.isnull().sum()

#############################################
# Çözüm 3: Tahmine Dayalı Atama ile Doldurma
#############################################

df = load()

cat_cols, num_cols, cat_but_car = grab_col_names(df)

num_cols = [col for col in num_cols if col not in "PassengerId"]
dff = pd.get_dummies(df[cat_cols + num_cols], drop_first=True)

dff.head()

# değişkenlerin standartlatırılması
scaler = MinMaxScaler()
dff = pd.DataFrame(scaler.fit_transform(dff), columns=dff.columns)
dff.head()


# knn'in uygulanması.
from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=5)
dff = pd.DataFrame(imputer.fit_transform(dff), columns=dff.columns)
dff.head()

#şu an dataframe imde standartlaştırılmış değerler var, bunların gerçek değerlerini geri almam lazım. bunu da "inverse transform" ile yapıyorum
dff = pd.DataFrame(scaler.inverse_transform(dff), columns=dff.columns)
dff.head()

#atadığım değerleri takip etmek için ilk df ime atadığım değerleri yeni bir kolon olarak atıyorum
df["age_imputed_knn"] = dff[["Age"]]
df.head()

df.loc[df["Age"].isnull(), ["Age", "age_imputed_knn"]]
df.loc[df["Age"].isnull()] #kıyaslamak için

###################
# Recap
###################

df = load()
# missing table
missing_values_table(df)
# sayısal değişkenleri direk median ile oldurma
df.apply(lambda x: x.fillna(x.median()) if x.dtype != "O" else x, axis=0).isnull().sum()
# kategorik değişkenleri mode ile doldurma
df.apply(lambda x: x.fillna(x.mode()[0]) if (x.dtype == "O" and len(x.unique()) <= 10) else x, axis=0).isnull().sum()
# kategorik değişken kırılımında sayısal değişkenleri doldurmak
df["Age"].fillna(df.groupby("Sex")["Age"].transform("mean")).isnull().sum()
# Tahmine Dayalı Atama ile Doldurma


#############################################
# Gelişmiş Analizler
#############################################

###################
# Eksik Veri Yapısının İncelenmesi
###################

msno.bar(df)
plt.show()

msno.matrix(df)
plt.show()

msno.heatmap(df)
plt.show()
#burada normal heatmap te olduğu gibi korelasyonu gösteriyor ama bu sefer boş değerler arasında ilişki olup olmadığını görebiliyoruz

###################
# Eksik Değerlerin Bağımlı Değişken ile İlişkisinin İncelenmesi
###################
#burası çok önemli. mesela cabin ile ilgili burada önemli bir analize erişiyoruz.
#kabin numarası olmayanların %30 u hayatta kalabiliyor, kabin numarası olanların hayatta kalma oranı %60 dır.
#burada veri bize bir şey anlatmak istiyor. aslında kabin numarası olmayanlar çalışanlarmış. hepsi değil ama çoğu.
#ve bunların haytta kalma oranı çok daha düşük.
#bir diğer önemli durum, eksik değerlerin sayısı da önemli buradaki oranları dikkate almak için.

missing_values_table(df, True)
na_cols = missing_values_table(df, True)


def missing_vs_target(dataframe, target, na_columns):
    temp_df = dataframe.copy()

    for col in na_columns:
        temp_df[col + '_NA_FLAG'] = np.where(temp_df[col].isnull(), 1, 0)

    na_flags = temp_df.loc[:, temp_df.columns.str.contains("_NA_")].columns

    for col in na_flags:
        print(pd.DataFrame({"TARGET_MEAN": temp_df.groupby(col)[target].mean(),
                            "Count": temp_df.groupby(col)[target].count()}), end="\n\n\n")


missing_vs_target(df, "Survived", na_cols)

###################
# Recap
###################

df = load()
na_cols = missing_values_table(df, True)
# sayısal değişkenleri direk median ile oldurma
df.apply(lambda x: x.fillna(x.median()) if x.dtype != "O" else x, axis=0).isnull().sum()
# kategorik değişkenleri mode ile doldurma
df.apply(lambda x: x.fillna(x.mode()[0]) if (x.dtype == "O" and len(x.unique()) <= 10) else x, axis=0).isnull().sum()
# kategorik değişken kırılımında sayısal değişkenleri doldurmak
df["Age"].fillna(df.groupby("Sex")["Age"].transform("mean")).isnull().sum()
# Tahmine Dayalı Atama ile Doldurma
missing_vs_target(df, "Survived", na_cols)