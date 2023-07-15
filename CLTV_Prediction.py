#Müşteri Yaşam Boyu Değeri Tahmini

#Customer Value = Purchase Frequency * Average Order Value

#Öyle bir şey yapmamız lazım ki, bütün kitlenin satınalma davranışları ve bütün kitlenin işlem başına ortalama
#bırakacağı kazancı olasılıksal olarak modelleyebileyim ve bu olasılıksal modelin üzerine bir kşinin özelliklerini girerek,
#genel kitle davranışlarından beslenerek bir tahmin işleminde bulunayım

#CLTV = Expected Number of Transaction * Expected Average Profit
#expected number of transaction: bütün kitlenin satınalma davranışını bir olasılık dağılımı ile modelleyeceğiz daha sonra bu davranış
#biçimlerini conditional(kişi başında) özelleştirerek her bir kişi için beklenen satınalma sayılarını tahmin edeceğiz
#Bu işlemleri yapacak 2 ayrı model var
#CLTV = BG/NBD Model * Gamma Gamma Submodel

##################################################
# BG/NBD (Beta Geometric / Negative Binomial Distribution) ile Expected Number of Transaction
##################################################
#expected: bir rassal değişkenin beklenen değeri, yani o rassal değişkenin ortalaması demek.
#rassal değişken: değerini bir deneyin sonuçlarından alan değişkene denir. yani bir değişkenin belirli bir olasılık
#dağılımı izlediğini varsaydığımızda, aslında o olasılık dağılımı izlediğini varsaydığımız değişkenin ortalaması demektir
#bu olasılık dağılımının beklenen değerini koşullandırarak, yani bireyler özelinde biçimlendirerek, her bir birey için beklenen işlem sayısını
#tahmin etmiş olacağız
#yani amacımız, olasılık dağılımları aracılığıyla, genel kitlenin satınalma davranışlarını modelleyip, bunları kişilerin özeline indirgemek

#CLTV = BG/NBD Model * Gamma Gamma Submodel

#BG/NBD modeli zaten tek başına "satın alma tahmin modeli" olarak kullanılan bir modeldir.
#Namı diğer: Buy Till You Die
#BG/NBD modeli, expected number of transaction için iki süreci olasılıksal olarak modeller: Transaction Process(Buy) + Dropout Process(Till You Die)

#TRANSACTION PROCESS(BUY)
#Alive olduğu sürece, belirli bir zaman periyodunda, bir müşteri tarafından gerçekleştirilecek işlem sayısı transaction rate parametresi
#ile poisson dağılır.

#Diğer deyişle, bir müşteri alive olduğu sürece kendi transaction rate'i etrafında rastgele satın alma yapmaya devam edecektir.

#Transaction rate'ler her bir müşteriye göre değişir ve tüm kitle için gamma dağılır (r, a)

#DROPOUT PROCESS(TILL YOU DIE)
#Her bir müşterinin p olasılığı ile dropout rate(dropout probability)i vardır.
#Bir müşteri alışveriş yaptıktan sonra belirli bir olasılıkla drop olur.
#Dropout rate ler her bir müşteriye göre değişir ve tüm kitle için beta dağılır (a, b)

#OZETLE, işlem oranı gamma dağılır, dropout lar beta dağılır

#Formülasyondaki x, t, T değerleri, her bir müşteri özelinde özelleştireceğimiz değerler
#r, a, a, b değerleri ise kitlemizden öğreneceğimiz olasılık dağılımı parametreleridir
#x: bir müşterinin tekrar eden satış sayısıdır
#t: bir müşterinin ilk satın alması ile son satın alması arasında geçen süre (haftalık cinsten) - müşteri özelindeki recency
#T: müşterinin ilk satınalması üzerinden geçen süre - müşterinin yaşı


##################################################
# Gamma Gamma Submodel
##################################################
#Bir müşterinin işlem başına ortalama ne kadar kar getirebileceğini tahmin etmek için kullanılır

#Bir müşterinin işlemlerinin parasal değeri (monetary) transaction value'larının ortalaması etrafında rastgele dağılır.
#Ortalama transaction value, zaman içinde kullanıcılar arasında değişebilir fakat tek bir kullanıcı için değişmez.
#Ortalama transaction value tüm müşteriler arasında gamma dağılır.

#Model değerlendirme
#x: frequency, tekrar eden satış sayısı, yani en az 2 kere işlem yapma şartını gerektiriyor
#mx: monetary, gözlemlenen transaction value ları. total price/toplam işlem sayısı
#diğer ifadeler: dağılımdan gelecek olan parametrelerdir
#formülasyon der ki, kişi ve dağılım özellikleri girildiğinde, monetary değerinin beklenen değerini verebilirim diyor. böylece
#mehmet beyin özelliklerini modele sorduğumuzda ortalama ne kadar karlılık bırakabileceğini belirtmiş olacak

#belirsizlik altında karar verebilmeyi geliştiriyoruz

#bu modelleri belirlediğimizde, CLTV nin tahmini değerlerini belirli bir zaman projeksiyonu ile ele almış olacağız


##################################################
# BG/NBD ve Gamma Gamma ile CLTV Tahmini
#(CLTV Prediction with BG-NBD & Gamma Gamma)
##################################################

# 1. Verinin Hazırlanması (Data Preperation)
# 2. BG-NBD Modeli ile Expected Number of Transaction
# 3. Gamma-Gamma Modeli ile Expected Average Profit
# 4. BG-NBD ve Gamma-Gamma Modeli ile CLTV'nin Hesaplanması
# 5. CLTV'ye Göre Segmentlerin Oluşturulması
# 6. Çalışmanın fonksiyonlaştırılması

##############################################################
# 1. Verinin Hazırlanması (Data Preperation)
##############################################################

# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.

# Veri Seti Hikayesi

# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler

# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.

##########################
# Gerekli Kütüphane ve Fonksiyonlar
##########################

!pip install lifetimes
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
from sklearn.preprocessing import MinMaxScaler

#kuracağımız modeller istatiksel modeller olduğundan dolayı, bu modelleri kurarken kullanacak olduğumuz değişkenlerin dağılımları, sonuçları
#direk etkileyecektir. bundan dolayı değişkenleri oluşturduktan spnra bu değişkenlerdeki aykırı değerlere dokunmamız gerekir.
#IQR-boxplot yöntemiyle önce aykırı değerleri tespit edicez, sonra aykırı değerleri baskılama yöntemi ile bu aykırı değerleri belirli
#bir eşik değeri ile değiştircez. Bunları 2 fonksiyonla yapacağız.

#kendisine girilen değişken için eşik değer belirlemek için:
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

#not: quantile larda normalde 0.25 ve 0.75 kullanılır fakat biz burada çok uç değerleri almak içn 0.01 ve 0.99 kullandık.

#uç değerleri yeni değerler ile baskıladığımız fonksiyon
def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    # dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

#########################
# Verinin Okunması
#########################

df_ = pd.read_excel("/Users/birsenbayat/Desktop/miuul/PythonProgrammingForDataScience/CRM_Analitigi/crmAnalytics/datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()
df.describe().T
df.isnull().sum()

#########################
# Veri Ön İşleme
#########################
#not: segmentasyonda aykırı değerlere odaklanmamıştık, burada odaklanacağız çünkü bir modelleme işlemi gerçekleştireceğiz. ve bu modeldeki
#yapılacak olan genellemelerde bazı sapmalara sebep olacaktır. bu sebeple eşik değerlerle değiştireceğiz
df.dropna(inplace=True)
df = df[~df["Invoice"].str.contains("C", na=False)]
df = df[df["Quantity"] > 0]
df = df[df["Price"] > 0]

replace_with_thresholds(df, "Quantity")
replace_with_thresholds(df, "Price")

df["TotalPrice"] = df["Quantity"] * df["Price"]
df.head()

today_date = dt.datetime(2011, 12, 11)

#########################
# Lifetime Veri Yapısının Hazırlanması
#########################

# recency: Son satın alma üzerinden geçen zaman. Haftalık. (kullanıcı özelinde)
# T: Müşterinin yaşı. Haftalık. (analiz tarihinden ne kadar süre önce ilk satın alma yapılmış)
# frequency: tekrar eden toplam satın alma sayısı (frequency>1)
# monetary: satın alma başına ortalama kazanç

cltv_df = df.groupby("Customer ID").agg({"InvoiceDate": [lambda x: (x.max() - x.min()).days,
                                                        lambda x: (today_date - x.min()).days],
                                         "Invoice": lambda x: x.nunique(),
                                         "TotalPrice": lambda x: x.sum()})
cltv_df.columns = cltv_df.columns.droplevel(0)
cltv_df.columns = ["recency", "T", "frequency", "monetary"]
cltv_df.head()

cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"] #sipiriş başına ortalama bırakılan gelir
cltv_df = cltv_df[(cltv_df["frequency"] > 1)]
cltv_df["recency"] = cltv_df["recency"] / 7 #haftalık değerini buluyoruz
cltv_df["T"] = cltv_df["T"] / 7 #haftalık değerini buluyoruz

cltv_df.describe().T

##############################################################
# 2. BG-NBD Modelinin Kurulması
##############################################################
#BetaGeoFitter: bir model nesnesi oluşturcam, bu model nesnesi aracılığıyla sen fit metodunu kullanarak freq, recency ve müşteri yaşı
#değerleini verdiğinde bu modeli kurmuş olcam der.
#parametre bulma işlemleri sırasında bir argümana ihtiyacım var der. bu parametre:
bgf = BetaGeoFitter(penalizer_coef=0.001) #modelin parametrelerinin bulunması aşamasında katsayılara uygulanacak olan ceza katsayısıdır
bgf.fit(cltv_df["frequency"],
        cltv_df["recency"],
        cltv_df["T"])

#şu an modelin detaylarına gerek yok fakat uzun süreli projelerde detaylara bakılmalıdır.

################################################################
# 1 hafta içinde en çok satın alma beklediğimiz 10 müşteri kimdir?
################################################################

bgf.conditional_expected_number_of_purchases_up_to_time(1,
                                                        cltv_df['frequency'],
                                                        cltv_df['recency'],
                                                        cltv_df['T']).sort_values(ascending=False).head(10)
#predict de kullanabiliriz
bgf.predict(1,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)

#not: diğer fonksiyon uzun diye predict kullandık fakat predict i gamma gamma da kullanamayız.

cltv_df["expected_purc_1_week"] = bgf.predict(1,
                                              cltv_df['frequency'],
                                              cltv_df['recency'],
                                              cltv_df['T'])

################################################################
# 1 ay içinde en çok satın alma beklediğimiz 10 müşteri kimdir?
################################################################

bgf.predict(4,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)

cltv_df["expected_purc_1_month"] = bgf.predict(4,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])

bgf.predict(4,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sum()

################################################################
# 3 Ayda Tüm Şirketin Beklenen Satış Sayısı Nedir?
################################################################

bgf.predict(4 * 3,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sum()

cltv_df["expected_purc_3_month"] = bgf.predict(4 * 3,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])

################################################################
# Tahmin Sonuçlarının Değerlendirilmesi
################################################################

plot_period_transactions(bgf)
plt.show()

##############################################################
# 3. GAMMA-GAMMA Modelinin Kurulması
##############################################################

ggf = GammaGammaFitter(penalizer_coef=0.01)

ggf.fit(cltv_df['frequency'], cltv_df['monetary'])

ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary']).head(10)


ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary']).sort_values(ascending=False).head(10)

cltv_df["expected_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                             cltv_df['monetary'])
cltv_df.sort_values("expected_average_profit", ascending=False).head(10)

##############################################################
# 4. BG-NBD ve GG modeli ile CLTV'nin hesaplanması.
##############################################################

cltv = ggf.customer_lifetime_value(bgf,
                                   cltv_df['frequency'],
                                   cltv_df['recency'],
                                   cltv_df['T'],
                                   cltv_df['monetary'],
                                   time=3,  # 3 aylık
                                   freq="W",  # T'nin frekans bilgisi.
                                   discount_rate=0.01)

cltv.head()

cltv = cltv.reset_index()

cltv_final = cltv_df.merge(cltv, on="Customer ID", how="left") #fonksiyon bu değere clv demiş, kafa karışmasına gerek yok aslında cltv değeridir.
cltv_final.sort_values(by="clv", ascending=False).head(10)


##############################################################
# 5. CLTV'ye Göre Segmentlerin Oluşturulması
##############################################################

cltv_final

cltv_final["segment"] = pd.qcut(cltv_final["clv"], 4, labels=["D", "C", "B", "A"])

cltv_final.sort_values(by="clv", ascending=False).head(50)

cltv_final.groupby("segment").agg(
    {"count", "mean", "sum"})



##############################################################
# 6. Çalışmanın Fonksiyonlaştırılması
##############################################################

def create_cltv_p(dataframe, month=3):
    # 1. Veri Ön İşleme
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    today_date = dt.datetime(2011, 12, 11)

    cltv_df = dataframe.groupby('Customer ID').agg(
        {'InvoiceDate': [lambda InvoiceDate: (InvoiceDate.max() - InvoiceDate.min()).days,
                         lambda InvoiceDate: (today_date - InvoiceDate.min()).days],
         'Invoice': lambda Invoice: Invoice.nunique(),
         'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

    cltv_df.columns = cltv_df.columns.droplevel(0)
    cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']
    cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"]
    cltv_df = cltv_df[(cltv_df['frequency'] > 1)]
    cltv_df["recency"] = cltv_df["recency"] / 7
    cltv_df["T"] = cltv_df["T"] / 7

    # 2. BG-NBD Modelinin Kurulması
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T'])

    cltv_df["expected_purc_1_week"] = bgf.predict(1,
                                                  cltv_df['frequency'],
                                                  cltv_df['recency'],
                                                  cltv_df['T'])

    cltv_df["expected_purc_1_month"] = bgf.predict(4,
                                                   cltv_df['frequency'],
                                                   cltv_df['recency'],
                                                   cltv_df['T'])

    cltv_df["expected_purc_3_month"] = bgf.predict(12,
                                                   cltv_df['frequency'],
                                                   cltv_df['recency'],
                                                   cltv_df['T'])

    # 3. GAMMA-GAMMA Modelinin Kurulması
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(cltv_df['frequency'], cltv_df['monetary'])
    cltv_df["expected_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                                 cltv_df['monetary'])

    # 4. BG-NBD ve GG modeli ile CLTV'nin hesaplanması.
    cltv = ggf.customer_lifetime_value(bgf,
                                       cltv_df['frequency'],
                                       cltv_df['recency'],
                                       cltv_df['T'],
                                       cltv_df['monetary'],
                                       time=month,  # 3 aylık
                                       freq="W",  # T'nin frekans bilgisi.
                                       discount_rate=0.01)

    cltv = cltv.reset_index()
    cltv_final = cltv_df.merge(cltv, on="Customer ID", how="left")
    cltv_final["segment"] = pd.qcut(cltv_final["clv"], 4, labels=["D", "C", "B", "A"])

    return cltv_final


df = df_.copy()

cltv_final2 = create_cltv_p(df)

cltv_final2.to_csv("cltv_prediction.csv")

#!!!!churn olmadıkça, müşterinin recency si arttıkça, satın alma olasılığı yükselir -> BG-NBD teorisi



















