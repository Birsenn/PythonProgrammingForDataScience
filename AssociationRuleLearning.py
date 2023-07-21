#Recommendation Systems
#kullanıcılara bazı teknikleri kullanarak ürün ya da hizmet önermek
#amaç: bol olan içerikleri filtrelemektir

##Simple Recommender System
# -kategorinin en yğksek puanlıları, bu hafta en çok izlenen filmler, trend olanlar vs. gibi...
# -iş bilgisi ve basit tekniklerle yapılabilen önerilerdir

##Association Rule Learning (Birliktelik Kuralı Öğrenimi)
#Sepet analizi de denir
# -birliktelik analizi ile öğrenilen kurallara göre ürün önerileri

##Content Based Filtering (İçerik Temelli Filtreleme)
# -ürün benzerliğine göre öneriler yapılan uzeklık temelli yöntemler

##Collaborative Filterin (İş Birlikçi Filtreleme)
# -topluluğun kullanıcı ya da ürün bazında ortak kanaatlerini yansıtan yöntemler
#User Based - Memory Based
#Item Based - Memory Based
#Model Based(Matrix Factorization) -Latent Methods

############################################
# ASSOCIATION RULE LEARNING (BİRLİKTELİK KURALI ÖĞRENİMİ)
############################################
#veri içerisindeki örüntüleri (pattern, ilişki, yapı) bulmak için kullanılan kural tabanlı bir makine öğrenmesi tekniğidir.
#walmart ın bebek bezleriyle bira satışı arasında bulduğu ilişki gibi
#mesela 8 alışveriş fişinin 5 inde ekmek ve süt birliktedir. 5/8-%60 civarlarında bu ürünler birlikte satın alınabilir

##### Apriori Algoritması
##########################
#Sepet analizi yöntemidir
#bu hesabı yapabilmek için 3 metric bilmemiz gerekir

#1: support(x, y) = freq(x, y) / N -> x ve ye nin birlikte satınalınma olasılığı
#2: confidence(x, y) = freq(x, y) / freq(x) -> x satın alındığında y nin satın alınma olasılığı
#3: lift = support(x, y) / (support(x) * support(y)) -> x satın alındığında y ürününün satın alınma olasılığı lift kadar artar

##### Association Rule Learning (Birliktelik Kuralı Öğrenimi)
#############################################################

# 1. Veri Ön İşleme
# 2. ARL Veri Yapısını Hazırlama (Invoice-Product Matrix)
# 3. Birliktelik Kurallarının Çıkarılması
# 4. Çalışmanın Scriptini Hazırlama
# 5. Sepet Aşamasındaki Kullanıcılara Ürün Önerisinde Bulunmak

############################################
# 1. Veri Ön İşleme
############################################

# !pip install mlxtend
import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
# çıktının tek bir satırda olmasını sağlar.
pd.set_option('display.expand_frame_repr', False)
from mlxtend.frequent_patterns import apriori, association_rules

df_ = pd.read_excel("/Users/birsenbayat/Desktop/miuul/PythonProgrammingForDataScience/Recommendation_Systems/recommender_systems/datasets/online_retail_II.xlsx",
                    sheet_name="Year 2010-2011")
df = df_.copy()
df.head()
df.shape

def retail_data_prep(dataframe):
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    return dataframe

df = retail_data_prep(df)
df.info()
df.describe().T

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

def retail_data_prep(dataframe):
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    return dataframe

df = retail_data_prep(df)
df.isnull().sum()

############################################
# 2. ARL Veri Yapısını Hazırlama (Invoice-Product Matrix)
############################################

df_fr = df[df["Country"] == "France"]
df_fr.groupby(["Invoice", "Description"]).agg({"Quantity": "sum"}).head()
df_fr.groupby(["Invoice", "Description"]).agg({"Quantity": "sum"}).unstack().iloc[0:5, 0:5]

#burada, fatura başına o üründen varsa 1, yoksa 0 yazdırıyoruz.
df_fr.groupby(['Invoice', 'StockCode']). \
    agg({"Quantity": "sum"}). \
    unstack(). \
    fillna(0). \
    applymap(lambda x: 1 if x > 0 else 0).iloc[0:5, 0:5]

def create_invoice_product_df(dataframe, id=False):
    if id:
        return dataframe.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)

fr_inv_pro_df = create_invoice_product_df(df_fr)

fr_inv_pro_df = create_invoice_product_df(df_fr, id=True)
fr_inv_pro_df.head()
fr_inv_pro_df.info()
def check_id(dataframe, stock_code):
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    print(product_name)

check_id(df_fr, 10120)

############################################
# 3. Birliktelik Kurallarının Çıkarılması
############################################

#lift: daha az sıklıkta olmasına rağmen o değerleri yakalayabilmektedir. dolayısı ile daha değerli ve yansız bir metriktir.
#leverage: lift gibidir fakat support u yüksek değerlere öncelik verme eğilimindedir, bundan dolayı yanlılığı vardır
#conviction: y olmadan x ürününün beklenen değeri, frekansıdır. veya tam tersi.


frequent_itemsets = apriori(fr_inv_pro_df,
                            min_support=0.01,
                            use_colnames=True)

frequent_itemsets.sort_values("support", ascending=False)

rules = association_rules(frequent_itemsets,
                          metric="support",
                          min_threshold=0.01)


rules[(rules["support"]>0.05) & (rules["confidence"]>0.1) & (rules["lift"]>5)]

check_id(df_fr, 21086)

rules[(rules["support"]>0.05) & (rules["confidence"]>0.1) & (rules["lift"]>5)]. \
sort_values("confidence", ascending=False)

############################################
# 4. Çalışmanın Scriptini Hazırlama
############################################

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

def retail_data_prep(dataframe):
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    return dataframe


def create_invoice_product_df(dataframe, id=False):
    if id:
        return dataframe.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)


def check_id(dataframe, stock_code):
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    print(product_name)

def create_rules(dataframe, id=True, country="France"):
    dataframe = dataframe[dataframe["Country"] == country]
    dataframe = create_invoice_product_df(dataframe, id)
    frequent_itemsets = apriori(dataframe, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
    return rules

df = df_.copy()

df = retail_data_prep(df)
rules = create_rules(df)

rules[(rules["support"]>0.05) & (rules["confidence"]>0.1) & (rules["lift"]>5)]. \
sort_values("confidence", ascending=False)

############################################
# 5. Sepet Aşamasındaki Kullanıcılara Ürün Önerisinde Bulunmak
############################################

#not: her defasında ürün bazında önerilecek ürün hesaplanmaz. gerçekleşecek senayorlara karşı çalışılır, ve hangi ürüne ne önerileceği bir
#tabloda tutulur. ordan müşteriye direk öneri gider.

# Örnek:
# Kullanıcı örnek ürün id: 22492

product_id = 22492
check_id(df, product_id)

sorted_rules = rules.sort_values("lift", ascending=False)

recommendation_list = []

for i, product in enumerate(sorted_rules["antecedents"]):
    for j in list(product):
        if j == product_id:
            recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

recommendation_list[0:3]

check_id(df, 22326)

def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

    return recommendation_list[0:rec_count]


arl_recommender(rules, 22492, 1)
arl_recommender(rules, 22492, 2)
arl_recommender(rules, 22492, 3)