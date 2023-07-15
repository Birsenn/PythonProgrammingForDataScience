#RFM Metrikleri: Recency, Frequency, Monetary
#RFM Analizi, müşteri segmentasyonu için kullanılan bir tekniktir
#Müşterilerin satınalma alışkanlıkları açısından gruplama ayrılması ve bu gruplar üzerinde stratejiler geliştirilebilmesini sağlar
#CRM çalışmaları için bir çok başlıkta veriye dayalı aksiyon alma imkanı sağlar

#Recency(Yenilik): müşterinin en son ne zaman alışveriş yaptığı durumunu ifade eder. müşterinin sıcaklığını, yeniliğini ifade eder
#Frequency(Sıklık): müşterinin satınalma/işlem sıklığıdır
#Monetary(Parasal Değer):

#Bu RFM metriklerini kıyaslanabilir yapmamız gerekir, yani RFM skorlarına çevirmemiz gerekir
#Bir başka deyişle, standartlaştırıyoruz. 1-5 arasında değerlere göre standartlaştırıyoruz. ve bu değerleri string olarak bir araya getirerek
#RFM değerlerini oluşturuyoruz (154 gibi). burada RFM skoru 555 olanlar en değerlidir diyebiliriz
#Fakat bunun sonucunda yine çok fazla varyasyona sahip RFM skorlar oluşur. Daha az sayıda bir skor, ayrımları mantıksal ve iş bilgisine uygun segmentler oluşturmalıyız

#Skorlar Üzerinden Segmentler Oluşturmak
#İki boyutlu görselde Recency ve Frequency var. Monetary neden yok?
#CRM analitiği çalışmaları kapsamında transaction-işlem daha önemlidir. Bu nedenle frekans daha önemlidir.

#UYGULAMA
#1- İş Problemi (Business Problem)
#2- Veriyi Anlama (Data Understanding)
#3- Veriyi Hazırlama (Data Preparation)
#4- RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
#5- RFM Skorlarının Hazırlanması (Calculating RFM Scores)
#6- RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
#7- Tüm Sürecin Fonksiyonlaştırılması

###############################################################
# 1. İş Problemi (Business Problem)
###############################################################

#e-ticaret şirketi var. bu şirket müşterilerini segmentlere ayırıp, bu segmentlere göre pazarlama stratejilerini belirlemek istiyor

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


###############################################################
# 2. Veriyi Anlama (Data Understanding)
###############################################################

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x) #Sayısal değişkenlerin virgülden sonra kaç basamağını görmek istiyorsam yazabilirim

df_ = pd.read_excel("/Users/birsenbayat/Desktop/miuul/PythonProgrammingForDataScience/CRM_Analitigi/crmAnalytics/datasets/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df = df_.copy()
df.head()
df.shape
df.isnull().sum() #customer bazında analiz yapacağım için buradaki Customer ID si null olanları sileceğim

#eşsiz ürün sayısı?
df["Description"].nunique()

#hangi üründen kaç tane satılmıştır?
df["Description"].value_counts().head()

#en çok sipariş edilen ürün hangisidir?
df.groupby("Description").agg({"Quantity":"sum"}).sort_values("Quantity", ascending=False).head()

#kaç tane fatura kesilmiş?
df["Invoice"].nunique()

#bir fatura için toplam tutar?
df["TotalPrice"] = df["Quantity"]*df["Price"]
df.groupby("Invoice").agg({"TotalPrice":"sum"}).sort_values("TotalPrice", ascending=False).head()


###############################################################
# 3. Veri Hazırlama (Data Preparation)
###############################################################
df.isnull().sum()
df.dropna(inplace=True)
df.shape

#not: burada aykırı değerleri atmak yoluna gitmeyebiliriz. Çümkü zaten bu aykırı değerler 5 e denk gelen değerler olacak.

df.describe().T

#veride eksi değer olduğunu görüyoruz. bu değerler iadelerden kaynaklanmaktadır.
#bu nedenle iade edilen faturaları veri setinden çıkarmamız lazım
#faturaların başında C olanların iade olduğu bilgisi vardı. içinde C olanları datasetten çıkarcam

df = df[~df["Invoice"].str.contains("C", na=False)]

###############################################################
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
###############################################################

#recency: analiz yapıldığı tarih - müşterinin son işlem tarihi
#frequency:  müşterinin yaptığı toplam satınalma
#monetary: toplam satınalmalar neticesinde bıraktığı toplam değerdir
df.head()

#analiz tarihini, son işlem tarihi üzerine 2 gün koyarak alabiliriz.
df["InvoiceDate"].max()

today_date = dt.datetime(2010, 12, 11) #tipini datetime a çevirdiğimizde, zaman açısından fark alabilmemizi sağlayacak

rfm = df.groupby("Customer ID").agg({"InvoiceDate": lambda invoicedate: (today_date - invoicedate.max()).days,
                                     "Invoice": lambda invoicecount: invoicecount.nunique(),
                                     "TotalPrice": lambda price: price.sum()})
rfm.head()

#değişkenlerin isimlerini değiştirmek istiyorum
rfm.columns = ["recency", "frequency", "monetary"]
rfm.head()
rfm.describe().T
rfm.shape

rfm = rfm[rfm["monetary"] > 0]


###############################################################
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
###############################################################

rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
#not: qcut küçükten büyüğe sıralar
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
#önemli not: frekansta valueerror alıyorum. sebebi böldüğm çeyrekliklere çok fazla aynı sayıdan giriyor olması. bu nedenle rank metodunu kullanmam gereiyor.
rfm.head()
rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str)+rfm["frequency_score"].astype(str))

rfm[rfm["RFM_SCORE"] == "55"]

###############################################################
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
###############################################################

#oluşturduğumuz skorları isimlendirmek için ve segmentlere ayırmak için regex kullanacağız

# RFM isimlendirmesi
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm["segment"] = rfm["RFM_SCORE"].replace(seg_map, regex=True)
rfm.head()

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

new_df = pd.DataFrame()
new_df["new_customer_id"] = rfm[rfm["segment"] == "new_customers"].index

new_df.head()

new_df["new_customer_id"] = new_df["new_customer_id"].astype(int)

new_df.to_csv("new_customers.csv")
rfm.to_csv("rfm.csv")


###############################################################
# 7. Tüm Sürecin Fonksiyonlaştırılması
###############################################################

def create_rfm(dataframe, csv=False):

    #VERIYI HAZIRLAMA
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]

    #RFM METRIKLERININ HESAPLANMASI
    today_date = dt.datetime(2011, 12, 11)
    rfm = dataframe.groupby("Customer ID").agg({"InvoiceDate": lambda date: (today_date-date.max()).days,
                                                "Invoice": lambda invoice: invoice.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    rfm.columns = ["recency", "frequency", "monetary"]
    rfm = rfm[(rfm["monetary"] > 0)]

    #RFM SKORLARININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

    rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))

    #RFM SEGMENTLERININ OLUŞTURULMASI
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm["segment"] = rfm["RFM_SCORE"].replace(seg_map, regex=True)
    rfm = rfm[["recency", "frequency", "monetary", "segment"]]
    rfm.index = rfm.index.astype(int)

    if csv:
        rfm.to_csv("rfm.csv")

    return rfm

df = df_.copy()

rfm_new = create_rfm(df)
rfm_new.head()

#bu analizler aydan aya yapılarak, müşteri segmentasyonu değişimlerinin takip edilmesi gerekiyor
