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


