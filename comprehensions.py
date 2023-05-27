#comprehensions: birden fazla satır ve kod ile yapılacak işlemleri istediğimiz veri
#yapısına göre kolayca gerçekleştirme imkanı sağlayan yapılardır

#List Comprehensions

#before
salaries = [1000, 2000, 3000, 4000, 5000]

for salary in salaries:
    salary = salary * 2
    print(salary)

#after
[salary * 2 for salary in salaries]

[salary * 2 for salary in salaries if salary < 3000]

[salary * 2 if salary < 3000 else salary * 0 for salary in salaries ]
#önemli: eğer if ve else birlikte kullanılacaksa for un saol tarafında yer alır
#eğer sadece if kullanılacaksa for un sağ tarafında yer alır

def new_salary(salary):
    return int(salary*0.2 + salary)

[new_salary(salary * 2) if salary < 3000 else salary * 0 for salary in salaries]
#burada artık fonksiyonu da list comprehension içine eklemiş olduk




students = ["John", "Mark", "Venessa", "Mariam"]

students_no = ["John", "Venessa"]

students = [student.lower() if student in students_no else student.upper() for student in students]
#gerçekten harika!!!
students

#nelerden kurtulduk??
#yeni bir liste oluşturmuyoruz, append yok, 4-5 satır kod yok


#######
#Dict Comprehensions

dictionary = {"a" : 1,
              "b" : 2,
              "c" : 3,
              "d" : 4}

dictionary.keys()
dictionary.values()
dictionary.items()

#:) hayat kurtaran serisi:
{k: v ** 2 for (k, v) in dictionary.items()} #sadece value ların karelerini alacak


{k.upper(): v for (k, v) in dictionary.items()} #sadece key leri büyük harf ile yazacak

{k.upper(): v * 2 for (k, v) in dictionary.items()} #hem key leri büyüttük, hem de value ları 2 ile çarptık

