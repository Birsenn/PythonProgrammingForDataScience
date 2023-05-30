# Neden Numpy?

import numpy as np

a = [1, 2, 3, 4, 5]
b = [2, 3, 4, 5, 6]

# bu iki listeyi nasıl çarparım

# uzun yol
ab = []
for i in range(0, len(a)):
    ab.append(a[i] * b[i])

# kısa yol (Numpy array)

a = np.array([1, 2, 3, 4, 5])
b = np.array([2, 3, 4, 5, 6])
a * b

#######
# Numpy Array Oluşturma

np.array([1, 2, 3, 4, 5])  # liste üzerinden bir numpy array
type(np.array([1, 2, 3, 4, 5]))

# sıfırdan array oluşturma
np.zeros(10, dtype=int)  # 10 tane sıfır içeren bir array oluşturdu

np.random.random_integers(0, 10, size=10)  # 0-10 arasında rastgele 10 tane integer seçti

np.random.normal(10, 4, (3, 4))  # ortalaması 10 olan, std si 4 olan 3-4 lük bir array oluşturdu

#######
# Numpy Array Özellikleri (Attributes of Numpy Arrays)

# ndim = boyut sayısı
# shape = boyut bilgisi
# size = toplam eleman sayısı
# dtype = array veri tipi

a = np.random.randint(10, size=5)
a.ndim
a.shape #satır ve sütun
a.size
a.dtype

#######
#Reshaping

np.random.randint(1,10, size=9).reshape(3,3) #dikkat: burada size ı 10 yapsaydık 3,3 lük çeviremeyeceği için hata alırdık!

#######
#Index Seçimi (Index Selection) !!!

a = np.random.randint(10, size=10)
a
a[0]
a[0:5]
a[0] = 999

m = np.random.randint(10, size=(3,5))
m

m[0,3] #ilk sayı satır, ikinci sayı sütunları temsil eder

m[2,3] = 999
m[2,3] = 2.9 #float bir veri göndermeye çalıştığımızda numpy bunu int olarak(2) alır çünkü tek tip veri tutar!!!
m

m[:,0] #bütün satırlardaki 0. sütunları al
m[0:2, 0:3]


#######
#Fancy Index

v = np.arange(0, 30, 3) #belli bir adımla array oluşturur. 0 dan 30 a kadar 3 er artarak array oluşturur.
v
catch = [1, 2, 3] #oluşturduğumuz listedeki sayıları index olarak alır ve v array indeki karşılıklarını getirir
v[catch]

#######
#Numpy'da Koşullu İşlemler (Conditions on Numpy)
v = np.array([1, 2, 3, 4, 5])

#3 ten küçük olan değerleri almak istiyorum
#Klasik döngü ile

ab = []
for i in v:
    if i < 3:
        ab.append(i)
ab

#Numpy ile
v < 3
v[v<3]
v[v == 3]
v[v != 3]

#kısaca bir array içinden istediğimiz değerleri yukarıdaki gibi kısa yolla (fancy index) alabiliriz

#######
#Matematiksel İşlemler (Mathematical Operations)

v/5
v*5 / 10
v ** 2
v - 1
#metodlar aracılığıyla da gerçekleştirebiliriz
np.subtract(v, 1)
np.add(v, 1)
np.mean(v)
np.max(v)
np.min(v)
np.sum(v)
np.var(v)

#Numpy ile İki Bilinmeyenli Denklem Çözümü

#5*x0 + x1 = 12
#x0 + 3*x1 = 10
#belli bir yapıda gönderirsek Numpy çözebilir

a = np.array([[5,1], [1,3]]) #katsayılar
b = np.array([12, 10]) #sonuçlar
np.linalg.solve(a, b)