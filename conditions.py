#if

number=10
if number == 10:
    print("number is 10")

#DRY prensibi: dont repeat yourself !!
#bu nedenle numara kontrolü için bir fonksiyon yazalım

def numbercheck(x):
    if number == 10:
        print("number is 10")

#######
#else

def numbercheck(number):
    if number == 10:
        print("number is 10")
    else:
        print("number is not 10")

numbercheck(12)

#######
#elif

def numbercheck(number):
    if number > 10:
        print("bigger than 10")
    elif number < 10:
        print("smaller than 10")
    else:
        print("number is 10")

numbercheck(10)

#######
#Loops

students = ["Jack", "Nelson", "Michael", "Monica", "Rachael"]

for student in students:
    print(student)


for student in students:
    print(student.upper())

salaries = [1000, 2000, 3000, 4000]

for salary in salaries:
    salary = salary + salary * 0.2
    print(int(salary))

#dont DRY!!

def new_salary(salary, percent):
    return int(salary*percent/100 + salary)

new_salary(2000, 10)

#salaries listesisnin tümüne bu fonksiyonu uygulamak için:

salaries = [1000, 2000, 3000, 4000]


for salary in salaries:
    if salary >= 3000:
        print(new_salary(salary, 10))
    else:
        print(new_salary(salary, 20))


#######
#break & continue & while
#döngülerle birlikte kullanılan bu yapılar, akışı kesmeye,
#ilgili şart gözlemlendiğinde o şartı atlayarak devam etmeye,
#ya da bir koşul sağlandığı sürece çalışmayı sürdürmeye yarayan ifadelerdir

salaries = [1000, 2000, 3000, 4000]

for salary in salaries:
    if salary == 3000:
        break
    print(salary)

for salary in salaries:
    if salary == 3000:
        continue       #sadece aranan koşulu (3000) es geçiyor.
    print(salary)


number = 1
while number < 5: #bir şart sağlandığı sürece çalışmayı sürdürür
    print(number)
    number += 1

#######
#Enumerate: Otomatik Counter/Indexer ile for loop

students = ["John", "Mark", "Venessa", "Mariam"]

for student in students:
    print(student)

for index, student in enumerate(students, 1): #buraya 1 yazdığımızda index 1 den başlar. istediğimiz değeri verebiliriz
    print(index, student)

A = []
B = []

for index, student in enumerate(students):
    if index %2 == 0:
        A.append(student)
    else:
        B.append(student)

print(A)
print(B)


#######
#Zip
#birbirinden farklı listeleri bir arada kullanabilmemizi sağlar

students = ["John", "Mark", "Venessa", "Mariam"]

departments = ["mathematics", "statistics", "physics", "astronomy"]

ages = [23, 30, 26, 22]

list(zip(students, departments, ages))


#######
#Lambda & Filter & Map & Reduce

#Lambda: kullan at fonksiyonlardır
#Map: for döngüsü yapmadan işlem yapmamızı sağlar.mesela istediğimiz fonksiyonu
#uygulayarak yeni bir lite oluşturmak istediğimizde bunu direk map ile yapabilriz

salaries = [1000, 2000, 3000, 4000]
list(map(lambda x: x * 20 / 100 + x, salaries))

#Filter: kullanımı azdır
list_store = [1,2,3,4,5,6,7,8,9,10]
list(filter(lambda x: x%2 == 0, list_store))

#Reduce
from functools import reduce

list_store = [1,2,3,4]
reduce(lambda a,b: a+b, list_store)

#not: bunlardan en önemlisi lambda ve map tir
#filter ve reduce ile kafa karıştırmaya gerek yok, sadece bilgi için verilmiştir
