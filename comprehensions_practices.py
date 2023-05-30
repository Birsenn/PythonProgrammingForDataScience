#Practice1
#Bir Veri Setindeki Değişken İsimlerini Değiştirmek

#before:
#["total", "spending", "alcohol", "not_distracted", "no_previous", ...]

#after:
#["TOTAL", "SPENDING", "ALCOHOL", "NOT_DISTRACTED", "NO_PREVIOUS", ...]

import seaborn as sns
df = sns.load_dataset("car_crashes")
df.columns
df

#burada hazır metodlar kullanmak yerine kendimiz yazdık

A = []
for col in df.columns:
    A.append(col.upper())

df.columns = A
df.columns

#ve şimdi de bunu list comprehension yolu ile yapacağız
df = sns.load_dataset("car_crashes")
df.columns = [col.upper() for col in df.columns]
df

#######
#Practice2
#İsminde INS olan değişkenlerin başına "FLAG", olmayanların başına "NO_FLAG" eklemek istiyoruz

df.columns = ["FLAG_" + col if "INS" in col else "NO_FLAG_" + col for col in df.columns]
df.columns

#######
#Practice3

#key'i string, values'su aşağıdaki gibi bir liste oluşturmak
#sadece sayısal değişkenler için yapmak istiyoruz

#{"total": ["mean", "min", "max", "var"]
# "speeding": ["mean", "min", "max", "var"]}
#....

#önce uzun yoldan yapacağız

import seaborn as sns
df = sns.load_dataset("car_crashes")
df.columns

#önce veri seti içerisindeki sayısal değişkenleri seçmemiz gerekiyor

num_cols = [col for col in df.columns if df[col].dtype != "O"]
num_cols
soz = {}
agg_list = ["mean", "min", "max", "sum"]

for col in num_cols:
    soz[col] = agg_list

soz

#kısa yol
new_dict = {col: agg_list for col in num_cols}

#hayat kurtaran kullanımı şu şekilde olabilir(ilerde daha iyi anlamak kaydıyşa)
df[num_cols].head()
df[num_cols].agg(new_dict)