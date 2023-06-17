#Case Studies
# 1: Verilen değerlerin veri yapılarını bulunuz
x = 8
y = 3.2
z = 8j + 18
a = "Hello AI Era"
b = True
c = 23 < 22
l = [1, 2, 3, 4]
d = {"Name":"Jake",
     "Age": 27,
     "Address": "Downtown"}
t = ("Machine Learning", "Data Science")
s = {"Python", "Machine Learning", "Data Science"}

#Çözüm
type(x) #int
type(y) #float
type(z) #complex
type(a) #str
type(b) #bool
type(c) #bool
type(l) #list
type(d) #dict
type(t) #tuple
type(s) #set

########################################################################
#2: Verilen string ifadenin tüm harflerini büyük harfe çeviriniz. Virgül ve nokta yerine space koyunuz, kelime kelime ayırınız.
# text = "The goal is to turn data into information, and information into insight"

def upperAndSpace(string):
    new_list = []
    string = string.replace(",", " ")
    string = string.replace(".", " ")
    string = string.split()
    for i in string:
        new_list.append(i.upper())
    return new_list

string = "The goal is to turn data into information, and information into insight."

#########################################################################################
#3: Verilenlisteyeaşağıdakiadımlarıuygulayınız.
#Adım 1: Verilen listenin eleman sayısına bakınız.
#Adım 2: Sıfırıncı ve onuncu indeksteki elemanları çağırınız.
#Adım 3: Verilen liste üzerinden ["D", "A", "T", "A"] listesi oluşturunuz.
#Adım 4: Sekizinci indeksteki elemanı siliniz.
#Adım 5: Yeni bir eleman ekleyiniz.
#Adım 6: Sekizinci indekse "N" elemanını tekrar ekleyiniz.

lst = ["D", "A", "T", "A", "S", "C", "I", "E", "N", "C", "E"]

len(lst) #1
lst[0]   #2
lst[10]  #2
new_list = lst[0:4] #3
lst.pop(8) #4
del lst[8] #4
#not: indekse göre eleman silerken pop veya del kullanabiliriz
lst.append("M") #5: en sona eleman ekler
lst.insert(2, "M") #indexe göre eleman ekler
lst.insert(8, "N") #6

#######################################################################################################
#4: Verilen sözlük yapısına aşağıdaki adımları uygulayınız.
#Adım 1: Key değerlerine erişiniz.
#Adım 2: Value'lara erişiniz.
#Adım 3: Daisy key'ine ait 12 değerini 13 olarak güncelleyiniz.
#Adım 4: Key değeri Ahmet value değeri [Turkey,24] olan yeni bir değer ekleyiniz.
#Adım 5: Antonio'yu dictionary'den siliniz.

dict = {"Christian": ["America", 18],
        "Daisy": ["England", 12],
        "Antonio": ["Spain", 22],
        "Dante": ["Italy", 25]}

dict.keys() #1
dict.values() #2
dict["Daisy"] = ["England", 13] #3
dict.update({"Daisy": ["England", 13]}) #3: update: eleman değiştirme yaparken ikinci yöntem, yeni bir eleman eklemek için de kullanılır
dict["Ahmet"] = ["Turkey", 24] #4
del dict["Antonio"] #5: 1.yöntem
dict.pop("Antonio") #5: 2.yöntem

###############################################################################################################
#5: Argüman olarak bir liste alan, listenin içerisindeki tek ve çift sayıları ayrı listelere atayan ve bu listeleri return eden fonksiyon yazınız.
l = [2, 3, 18, 93, 22]
def func(liste):
    even_list = []
    odd_list = []
    for i in liste:
        if i %2 == 0:
            even_list.append(i)
        else:
            odd_list.append(i)
    return even_list, odd_list

even_list, odd_list = func(l)

#################################################################################################
#6: Aşağıda verilen listede mühendislik ve tıp fakülterinde dereceye giren öğrencilerin isimleri bulunmaktadır. Sırasıyla ilk üç öğrenci mühendislik fakültesinin başarı sırasını temsil ederken son üç öğrenci de tıp fakültesi öğrenci sırasına aittir.
#Enumarate kullanarak öğrenci derecelerini fakülte özelinde yazdırınız.
ogrenciler = ["Ali", "Veli", "Ayşe", "Talat", "Zeynep", "Ece"]

for i, ogrenci in enumerate(ogrenciler, 1):
    if i < 4:
        print(f"Mühendislik Fakültesi {i}. ogrenci: {ogrenci}")
    else:
        print(f"Tıp Fakültesi {i}. ogrenci: {ogrenci}")

#tek seferde başarı:)
#şimdi bir de fonskyion olarak tanımlayalım

def fakulteDerece(liste):
    for i, ogrenci in enumerate(liste, 1):
        if i <4:
            print(f"Mühendislik Fakültesi {i}. ogrenci: {ogrenci}")
        else:
            print(f"Tıp Fakültesi {i}. ogrenci: {ogrenci}")

fakulteDerece(ogrenciler)

########################################################################################################
#7: Aşağıda 3 adet liste verilmiştir.
#Listelerde sırası ile bir dersin kodu, kredisi ve kontenjan bilgileri yer almaktadır. Zip kullanarak ders bilgilerini bastırınız.

ders_kodu = ["CMP1005", "PSY1001", "HUK1005", "SEN2204"]
kredi = [3, 4, 2, 4]
kontenjan = [30, 75, 150, 25]

new_list = list(zip(ders_kodu, kredi, kontenjan))

for i in new_list:
    print(f"Kredisi {i[1]} olan {i[0]} dersin kontenjanı {i[2]} kişidir.")

#yine tekte başarı çok şükür:) şimdi fonksiyonunu yazalım.

def dersBilgileri(ders_kodu, kredi, kontenjan):
    new_list = list(zip(ders_kodu, kredi, kontenjan))
    for i in new_list:
        print(f"Kredisi {i[1]} olan {i[0]} dersin kontenjanı {i[2]} kişidir.")


#############################################################################################
#8: Aşağıda 2 adet set verilmiştir. Sizden istenilen eğer 1. küme 2.
#kümeyi kapsiyor ise ortak elemanlarını eğer kapsamıyor ise 2. kümenin 1. kümeden farkını yazdıracak fonksiyonu tanımlamanız beklenmektedir.

kume1 = set(["data", "python"])
kume2 = set(["data", "function", "qcut", "lambda", "python", "miuul"])

def kume(kume1, kume2):
    if kume1.issuperset(kume2) == True:
        print(kume2.intersection(kume1))
    else:
        print(kume2.difference(kume1))

##############################################################################################
