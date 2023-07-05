import math
#eval(): aldığımız işlemi direk çıktı olarak verir, yani değeri python kodu olarak işler.
#mesela ben aşağıda birinci değişkene 5*3 yazdığımda a ya direk 15 diyor.
#fakat eval siz yazdırdığımda "5*3" olarak yazar.
import math
a = eval(input("Birinci değişken: "))
5*3

###############################################################################################
#1-dik üçgenin 3. kenarını hesaplama
a = int(input("1. dik kenar: "))
b = int(input("2. dik kenar: "))

c = (a**2 + b**2)**0.5
print(c)
3

###############################################################################################
#2-iki kenarı ve bunlar arasındaki açısı verilen bir üçgenin diğer kenarını hesaplama
a= int(input("1.kenar: "))
b= int(input("2.kenar: "))
D= int(input("degree: "))

c = (a**2 + b**2 -2*a*b*math.cos(D))**0.5
print(c)

###############################################################################################
#3-girilen sayının tek mi çift mi olduğunu bulma
a = int(input())
if a %2 ==0:
    print("çift sayı")
else:
    print("tek sayı")

###############################################################################################
#4-pozitif bir tamsayının tam bölenlerini hesaplayınız
b= int(input())
print(b)
print(1)
for i in range(2, int(b/2+1)): #burada fazladan işlem yapılmasını engellemek için sayının yarısı alınmıştır. çünkü sayılar kendi yarısından daha büyük bir tam sayıya tam bölünemez(kendisi hariç)
    if b %i == 0:
        print(i)

###############################################################################################
#5-verilen bir n sayısına göre, 1'den n'e kadar olan tamsayıların toplamını t1, 1'den n'e kadar olan tek tamsayıların toplamını t2,
#1'den n'e kadar olan çift tamsayıların toplamını t3 olarak hesaplayınız.
n = 50
t1=t2=t3=0
for i in range(1, n+1):
    if i %2 != 0:
        t2 += i
    else:
        t3 += i
    return t2, t3 #return neden çalışmıyor?

#2.yöntem
t1 = sum(range(1, n+1, 1))
t2 = sum(range(1, n+1, 2))
t3 = sum(range(2, n+1, 2))

print(f"bütün sayıların toplamı: {t1} \ntek sayıların toplamı: {t2} \nçift sayıların toplamı: {t3}.")

###############################################################################################
#6-Eleman sayısı girilen bir kümenin belirtilen kombinasyonlarının sayısını hesaplayınız.
#bilgi: n elemanlı bir kümenin r'li kombinasyonlarının sayısı k=f1/(f2*f3) tür
#f1 = n!, f2 = r!, f3 = (n-r)!

n=6
r=2
f1 = f2 = f3 = 1
for i in range(1, n+1):
    f1 *= i
    if i <= r:
        f2 *= i
    if i <= (n-r):
        f3 *= i
k = f1/(f2*f3)
print(k)

###############################################################################################
#7-A != 0 olmak üzere klavyeden katsayıları girilen ikinci dereceden denklemin köklerini hesaplayan program
ax2 + bx + c = 0
a=1
b=4
c=4

D = (b**2 - (4*a*c))**0.5
if D == 0:
    x = -b/2*a
    print(x)
if D > 0:
    x1 = (-b - D**0.5)/2*a
    x2 = (-b + D**0.5)/2*a
    print(x1, x2)
if D < 0:
    print("Sanal Kökler")


###############################################################################################
#8-Katsayıları girilen ax2+bx+c = 0 ikinci dereceden denklemin köklerini a+b+c = 0 olması durumunda diskriminant hesaplamadan çözen program.
#not: bu koşulu sağlayan denklemin kökleri her zaman 1 ve c/a dır.
a=2
b=-1
c=1
if a+b+c == 0:
    x1 = 1
    x2 = c/a
    print(x1, x2)
else:
    print(False)

###############################################################################################
#9-metre cinsinden girilen uzunluğu, seçilen birime dönüştüren program
a=100
print("""
1-mm
2-cm
3-dm
4-km""")
x = eval(input("Lütfen çevirmek istediğiniz birimi giriniz: "))

if x == 1:
    b = a*1000
elif x == 2:
    b = a*100
elif x == 3:
    b = a*10
elif x == 4:
    b = a/1000
print(b)


###############################################################################################
#10-seçilen mevsime göre ay isimlerini listeleyen program

print("""Ay İsimleri:
1-İlkbahar
2-Yaz
3-Sonbahar
4-Kış
""")
secim = eval(input("Lütfen ayı seçiniz: "))

if secim == 1:
    print("Mart, Nisan, Mayıs")
elif secim == 2:
    print("Haziran, Temmuz, Ağustos")
elif secim == 3:
    print("Eylül, Ekim, Kasım")
elif secim == 4:
    print("Aralık, Ocak, Şubat")

###############################################################################################






