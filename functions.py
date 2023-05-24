#######
# Fonksiyon Tanımlama

def calculate(x):
    print(x * 2)


calculate(10)

#######
#İki Argümanlı/Parametreli Bir Fonksiyon Tanımlamak

def summer(arg1, arg2):
    print(arg1 + arg2)

summer(7, 8) #burada arg ların sıralaması önemlidir

###############
#Docstring
#fonksiyonlarımıza,herkesin anlayacağı şekilde bilgi notu ekleme yoludur

#docstring eklemek için en yaygın kullanılan iki yol: Numpy ve Google
#bunu ayarlamak için: Menu-Preferences-Aramaya docstring yaz-Tools un altındaki bölüme tıkla-docstring format tan seç


def summer(arg1, arg2):
    """
    Sum of two numbers

    Parameters/Args
    :param arg1: int, float
    :param arg2: int, float
    :return: int, float
    """
    print(arg1 + arg2)


#######
#Fonksiyonların Statement/Body Bölümü

def say_hi(string):
    print(string)  #istersek atama yapıp sonradan yazabiliriz
    print("Hello") #istersek direk bir input verebiliriz

say_hi("birsen")

#######
#Girilen Değerleri Bir Liste İçinde Tutacak Fonksiyon

list = []
def listkeep(a, b):
    c = a * b
    list.append(c)
    print(list)

listkeep(5, 8)

#######
#Default Arguments/Parameters

def say_hi(string="Merhaba"):
    print(string)

say_hi() #default bir parametre tanımladığımızda arguman girmeden de fonksiyonu çalıştırabiliriz

#######
#Return: Fonksiyon Çıktılarını Girdi Olarak Kullanmak

def calculate(warm, moisture, charge):
    warm = warm * 2
    moisture = moisture * 2
    charge = charge * 2
    output = (warm+moisture) / charge
    return warm, moisture, charge, output

warm, moisture, charge, output = calculate(25, 46, 65)


#######
#fonksiyon içerisinden fonksiyon çağırmak

def calculate(warm, moisture, charge):
    return int((warm + moisture) / charge)

def standardization(a, p):
    return a * 10 / 100 * p * p

def all_calculation(warm, moisture, charge, p):
    a = calculate(warm, moisture, charge) #fonksiyon içinde fonksiyon
    b = standardization(a, p)             #fonksiyon içinde fonksiyon
    print(b * 10)

all_calculation(26, 43, 65, 6)

#Global ve Local Değişkenler

#yukarıdaki fonksiyonda a local değişkendir, warm ise global değişkendir.
#local değişkenleri sağ alt köşedeki bölümde göremeyiz

















