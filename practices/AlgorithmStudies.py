import math
#eval(): aldığımız işlemi direk çıktı olarak verir, yani değeri python kodu olarak işler.
#mesela ben aşağıda birinci değişkene 5*3 yazdığımda a ya direk 15 diyor.
#fakat eval siz yazdırdığımda "5*3" olarak yazar.
import math
a = eval(input("Birinci değişken: "))
5*3

###############################################################################################
#dik üçgenin 3. kenarını hesaplama
a = int(input("1. dik kenar: "))
b = int(input("2. dik kenar: "))

c = (a**2 + b**2)**0.5
print(c)
3

###############################################################################################
#iki kenarı ve bunlar arasındaki açısı verilen bir üçgenin diğer kenarını hesaplama
a= int(input("1.kenar: "))
b= int(input("2.kenar: "))
D= int(input("degree: "))

c = (a**2 + b**2 -2*a*b*math.cos(D))**0.5
print(c)

###############################################################################################