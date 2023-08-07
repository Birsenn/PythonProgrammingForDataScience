#Amaç: sınıflandırma problemi için bağımlı ve bağımsız değişkenler arasındaki ilşkiyi doğrusal olarak modellemektir.
#Sigmoid fonksiyonunun görevi: çıktıyı 0-1 arasına eşlemek
#Nasıl?
#Gerçek değerler ile tahmin edilen değerler arasındaki farklara ilişkin log loss değerini minimum yapacak ağırlıkları bularak

#aslında 1 sınıfına ait olma olasılığını elde ederiz ve bu 1 sınıfına ait olma olasılığını eşik değerine göre dönüştürürüz.
#doğrusal ve logistic regresyondaki bu dönüşüm işlemi, makine öğrenmesi ve derin öğrenmenin temelini oluşturmaktadır.

#entropy: ne kadar yüksekse çeşitlilik o kadar fazladır. gerçek değer ile tahmin edilen değer açısından entropinin düşük olmasını isteriz

#Başarı Değerlendirme Metrikleri
#Confusion matrix
#accuracy (her zaman kullanılmamalıdır): doğru sınıflandırma oranı
#precision: pozitif sınıf tahminlerinin başarı oranı (buradaki hatalı tahminlere tip 1 hatası denir, bu hata çok büyük problem değildir)
#recall: pozitif sınıfın doğru tahmin edilme oranı (sahtekarlık işlemlerinin ne kadarının doğru tahmin edildiğini ifade eder,
#burada hata büyüktür. olanları yakalayamamak sıkıntılıdır. para veya can kaybı yaşanabilir. Tip 2 hatası ve kritik hatadır)
#f1 scoru: precision ve recall un harmonik ortalamasıdır.

#!!!!!!!!!!!!!!!!!!!!!!!
#nasıl kullanacağız?
#eğer elimizdeki sınıflandırma problemi dengeli sınıf dağılımına sahipse, direk accuracy yi verebiliriz
#ama dengesizse accuracy kullanamayız, precision ve recall kullanmalıyız


#Threshould
#Classification threshould, her zaman 0.5 kabul edilir.
#threshould değiştikçe diğer bütün metriklerin değerleri değişir
#peki o zaman ne yapmak gerekir???

#ROC CURVE kullanmalıyım (Receiver Operating Characteristic Curve)
#olası bütün threshould değerlerine göre confusion matrix in hespalanması sonucunda çıkan eğri

#Area Under Curve (AUC)
#ROC eğrisinin sayısal bir şekilde ifade edilmesidir
#ROC eğrisi altında kalan alandır
#AUC, tüm olası sınıflandırma eşikleri için toplu bir performans ölçüsüdür


#LOG Loss
#sınıflandırma problemleri için bir başarı metriğidir
#hem de optimize edilmek üzere objective function dır, amaç fonksiyonumuzdur. düşmesini bekleidğimiz fonksiyondur.

#Scaling
#doğrusal ve uzaklık temelli yöntemlerde ve gradient descent kullanan yöntemlerde standartlaştırma işlemleri önemlidir. Neden?
#1-modellerin değişkenlere eşit yaklaşmasını sağlamamız gerekir (sumocu-çocuk örneği)
#2-kullanılan parametre tahmin yöntemlerinin daha hızlı ve daha doğru tahminlerde bulunması için

#Robust Scaler: en önemli özelliği aykırı değerlerden etkilenmemesi, daha robust olmasıdır.
#bunun nedeni median ı baz alarak işlem yapmasıdır
#istersen diğerlerini de tek tek deneyip en iyi sonucu aldığın yöntemi kullanabilirsin






######################################################
# Diabetes Prediction with Logistic Regression
######################################################

# İş Problemi:

# Özellikleri belirtildiğinde kişilerin diyabet hastası olup
# olmadıklarını tahmin edebilecek bir makine öğrenmesi
# modeli geliştirebilir misiniz?

# Veri seti ABD'deki Ulusal Diyabet-Sindirim-Böbrek Hastalıkları Enstitüleri'nde tutulan büyük veri setinin
# parçasıdır. ABD'deki Arizona Eyaleti'nin en büyük 5. şehri olan Phoenix şehrinde yaşayan 21 yaş ve üzerinde olan
# Pima Indian kadınları üzerinde yapılan diyabet araştırması için kullanılan verilerdir. 768 gözlem ve 8 sayısal
# bağımsız değişkenden oluşmaktadır. Hedef değişken "outcome" olarak belirtilmiş olup; 1 diyabet test sonucunun
# pozitif oluşunu, 0 ise negatif oluşunu belirtmektedir.

# Değişkenler
# Pregnancies: Hamilelik sayısı
# Glucose: Glikoz.
# BloodPressure: Kan basıncı.
# SkinThickness: Cilt Kalınlığı
# Insulin: İnsülin.
# BMI: Beden kitle indeksi.
# DiabetesPedigreeFunction: Soyumuzdaki kişilere göre diyabet olma ihtimalimizi hesaplayan bir fonksiyon.
# Age: Yaş (yıl)
# Outcome: Kişinin diyabet olup olmadığı bilgisi. Hastalığa sahip (1) ya da değil (0)


# 1. Exploratory Data Analysis
# 2. Data Preprocessing
# 3. Model & Prediction
# 4. Model Evaluation
# 5. Model Validation: Holdout
# 6. Model Validation: 10-Fold Cross Validation
# 7. Prediction for A New Observation


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, classification_report, plot_roc_curve
from sklearn.model_selection import train_test_split, cross_validate

def outlier_thresholds(dataframe, col_name, q1=0.05, q3=0.95):
    quartile1 = dataframe[col_name].quantile(q1)
    quartile3 = dataframe[col_name].quantile(q3)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def check_outlier(dataframe, col_name):
    low_limit, up_limit = outlier_thresholds(dataframe, col_name)
    if dataframe[(dataframe[col_name] > up_limit) | (dataframe[col_name] < low_limit)].any(axis=None):
        return True
    else:
        return False

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 500)



######################################################
# Exploratory Data Analysis
######################################################

df = pd.read_csv("datasets/diabetes.csv")

##########################
# Target'ın Analizi
##########################

df["Outcome"].value_counts()

sns.countplot(x="Outcome", data=df)
plt.show()

100 * df["Outcome"].value_counts() / len(df)

##########################
# Feature'ların Analizi
##########################

df.head()

df["BloodPressure"].hist(bins=20)
plt.xlabel("BloodPressure")
plt.show()

def plot_numerical_col(dataframe, numerical_col):
    dataframe[numerical_col].hist(bins=20)
    plt.xlabel(numerical_col)
    plt.show(block=True)


for col in df.columns:
    plot_numerical_col(df, col)

cols = [col for col in df.columns if "Outcome" not in col]


# for col in cols:
#     plot_numerical_col(df, col)

df.describe().T

##########################
# Target vs Features
##########################

df.groupby("Outcome").agg({"Pregnancies": "mean"})

def target_summary_with_num(dataframe, target, numerical_col):
    print(dataframe.groupby(target).agg({numerical_col: "mean"}), end="\n\n\n")

for col in cols:
    target_summary_with_num(df, "Outcome", col)



######################################################
# Data Preprocessing (Veri Ön İşleme)
######################################################
df.shape
df.head()

df.isnull().sum()

df.describe().T

for col in cols:
    print(col, check_outlier(df, col))

replace_with_thresholds(df, "Insulin")

for col in cols:
    df[col] = RobustScaler().fit_transform(df[[col]])

df.head()


######################################################
# Model & Prediction
######################################################

y = df["Outcome"]

X = df.drop(["Outcome"], axis=1)

log_model = LogisticRegression().fit(X, y)

log_model.intercept_
log_model.coef_

y_pred = log_model.predict(X)

y_pred[0:10]

y[0:10]



######################################################
# Model & Prediction
######################################################

y = df["Outcome"]

X = df.drop(["Outcome"], axis=1)

log_model = LogisticRegression().fit(X, y)
log_model.intercept_
log_model.coef_

y_pred = log_model.predict(X)
y_pred[0:10]

y[0:10]


######################################################
# Model Evaluation
######################################################

def plot_confusion_matrix(y, y_pred):
    acc = round(accuracy_score(y, y_pred), 2)
    cm = confusion_matrix(y, y_pred)
    sns.heatmap(cm, annot=True, fmt=".0f")
    plt.xlabel('y_pred')
    plt.ylabel('y')
    plt.title('Accuracy Score: {0}'.format(acc), size=10)
    plt.show()

plot_confusion_matrix(y, y_pred)

print(classification_report(y, y_pred))


# Accuracy: 0.78
# Precision: 0.74
# Recall: 0.58
# F1-score: 0.65

# ROC AUC
y_prob = log_model.predict_proba(X)[:, 1]
roc_auc_score(y, y_prob)
# 0.83939


######################################################
# Model Validation: Holdout
######################################################

X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.20, random_state=17)

log_model = LogisticRegression().fit(X_train, y_train)

y_pred = log_model.predict(X_test)
y_prob = log_model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))

# Accuracy: 0.78
# Precision: 0.74
# Recall: 0.58
# F1-score: 0.65

# Accuracy: 0.77
# Precision: 0.79
# Recall: 0.53
# F1-score: 0.63

plot_roc_curve(log_model, X_test, y_test)
plt.title('ROC Curve')
plt.plot([0, 1], [0, 1], 'r--')
plt.show()

# AUC
roc_auc_score(y_test, y_prob)

#Notlar:
#random state i değiştirerek modeli denediğimiz bu iki yöntemde, precision ve recall artarken accuracy aynı kaldı.
#yani test-train veri seti değiştikçe model sonucu farklı çıkıyor. modele güvenemem, bu noktada "k fold cross validation"



######################################################
# Model Validation: 10-Fold Cross Validation
######################################################

y = df["Outcome"]
X = df.drop(["Outcome"], axis=1)

log_model = LogisticRegression().fit(X, y)

cv_results = cross_validate(log_model,
                            X, y,
                            cv=5,
                            scoring=["accuracy", "precision", "recall", "f1", "roc_auc"])



# Accuracy: 0.78
# Precision: 0.74
# Recall: 0.58
# F1-score: 0.65

# Accuracy: 0.77
# Precision: 0.79
# Recall: 0.53
# F1-score: 0.63


cv_results['test_accuracy'].mean()
# Accuracy: 0.7721

cv_results['test_precision'].mean()
# Precision: 0.7192

cv_results['test_recall'].mean()
# Recall: 0.5747

cv_results['test_f1'].mean()
# F1-score: 0.6371

cv_results['test_roc_auc'].mean()
# AUC: 0.8327

######################################################
# Prediction for A New Observation
######################################################

X.columns

random_user = X.sample(1, random_state=45)
log_model.predict(random_user)