#Customer Lifetime Value(Müşteri Yaşam Boyu Değeri)
#Bir müşterinin bir şirketle kurduğu ilişki-iletişim süresince bu şirkete kazandıracağı parasal değerdir
#Neden öenmlidir?
#Şirket için orta-uzun vadeli, katma değer odaklı bir yaklaşım sergileyebiliriz, hem de müşterilerle olan ilişkilerimizi düzenleyebiliriz
#Bu durum aynı zamanda, pazarlama faaliyetleri için belirlenecek bütçelerin belirlenmesinde de önemli rol oynayacaktır
#Elimizdeki müşterilerin lifetime value larını hesaplayabilirsek, bir diğer endişe olan yeni müşteri bulma çabasının da maliyetlerini birimleştirebilirsek,
#bu durumda iki durumu kıyaslayabilecek bilgi edinmiş oluruz.

#Nasıl hesaplanır?
#satın alma başına ortalama kazanç * satın alma sayısı

#CLTV = (Customer Value/Churn Rate)*Profit Margin
#Customer Value = Average Order Value*Purchase Frequency
#Average Order Value(satın alma başına ortalama kazanç) = Total Price/Total Transaction
#Purchase Frequency = Total Transaction/Total Number of Customers
#Churn Rate = 1-Repeat Rate
#Profit Margin = Total Price*0.1

############################################
# CUSTOMER LIFETIME VALUE (Müşteri Yaşam Boyu Değeri)
############################################

# 1. Veri Hazırlama
# 2. Average Order Value (average_order_value = total_price / total_transaction)
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
# 5. Profit Margin (profit_margin =  total_price * 0.10)
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
# 8. Segmentlerin Oluşturulması
# 9. BONUS: Tüm İşlemlerin Fonksiyonlaştırılması

##################################################
# 1. Veri Hazırlama
##################################################

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

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_ = pd.read_excel("/Users/birsenbayat/Desktop/miuul/PythonProgrammingForDataScience/CRM_Analitigi/crmAnalytics/datasets/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df = df_.copy()

df = df[~df["Invoice"].str.contains("C", na=False)]
df = df[(df["Quantity"] > 0)]
df.dropna(inplace=True)
df.describe().T #eksi değerleri kaldırdıktan sonra price ortalaması da düştü, bunu inceleyebilirsin


df["TotalPrice"] = df["Quantity"] * df["Price"]


#gerekli metriklerin hesaplanması: total price, total transaction
cltv_c = df.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                        'Quantity': lambda x: x.sum(),
                                        'TotalPrice': lambda x: x.sum()})



cltv_c.columns = ["total_transaction", "total_unit", "total_price"]
cltv_c["total_price"].max()
#not: buradaki total_transaction, rfm deki frequency değerine eşittir. total_price değeri de monetary değerine eşittir.
#fakat literaturde ifade ediliş şekilleri bu şekildedir

##################################################
# 2. Average Order Value (average_order_value = total_price / total_transaction)
##################################################

cltv_c["average_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"]

##################################################
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
##################################################

cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]
cltv_c.head()

##################################################
# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
##################################################

repeat_rate = (cltv_c[cltv_c["total_transaction"] > 1]).shape[0] / cltv_c.shape[0]
churn_rate = 1-repeat_rate

##################################################
# 5. Profit Margin (profit_margin =  total_price * 0.10)
##################################################

cltv_c["profit_margin"] = cltv_c["total_price"] * 0.1

##################################################
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
##################################################

cltv_c["customer_value"] = cltv_c["average_order_value"] * cltv_c["purchase_frequency"]

##################################################
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
##################################################

cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"]

cltv_c.sort_values(by="cltv", ascending=False).head()

cltv_c.describe().T

##################################################
# 8. Segmentlerin Oluşturulması
##################################################

#oluşturduğumuz bu cltv değeri ile artık odaklanmam gereken müşteri segmentini bulabilirim.
#tek bir kritere indirgedim fakat ne kadarına odaklanmam gerektiğini bilmiyorum. Mesela 4 gruba-segmente ayırabilirim.

cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])
cltv_c.sort_values(by="cltv", ascending=False).head()

#segmentleri oluşturduk. peki bu segmentler mantıklı mı? analiz etmek gerekiyor.

cltv_c.groupby("segment").agg(["count", "mean", "sum"])

cltv_c.to_csv("cltv_c.csv")

##################################################
# 9. BONUS: Tüm İşlemlerin Fonksiyonlaştırılması
##################################################

def create_cltv_c(dataframe, csv=False):

    #VERIYI HAZIRLAMA
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe.dropna(inplace=True)
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    cltv_c = dataframe.groupby("Customer ID").agg({"Invoice": lambda x: x.nunique(),
                                            "TotalPrice": lambda x: x.sum(),
                                            "Quantity":lambda x: x.sum()})

    cltv_c.columns = ["total_transaction", "total_price", "total_unit"]

    #GEREKLI METRIKLERIN HESAPLANMASI
    #average order value
    cltv_c["average_order_value"] = cltv_c["total_price"]/cltv_c["total_transaction"]

    #purchase frequency
    cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]

    #repeat rate&churn rate
    repeat_rate = cltv_c[cltv_c["total_transaction"]>1].shape[0] / cltv_c.shape[0]
    churn_rate = 1 - repeat_rate

    #profit margin
    cltv_c["profit_margin"] = cltv_c["total_price"]*0.1

    #customer value
    cltv_c["customer_value"] = cltv_c["average_order_value"] * cltv_c["purchase_frequency"]

    #customer lifetime value
    cltv_c["cltv"] = (cltv_c["customer_value"]/churn_rate) * cltv_c["profit_margin"]

    #SEGMENTLERIN OLUŞTURULMASI
    cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

    if True:
        cltv_c.to_csv("cltv_c.csv")

    return cltv_c

df = df_.copy()

create_cltv_c(df).head()









