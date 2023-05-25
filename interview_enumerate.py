#divide_students fonksiyonu yazınız
#çift indexe sahip öğrencileri bir listeye alınız
#tek indexe sahip öğrencileri bir listeye alınız
#fakat bu iki liste tek bir liste olarak return olsun


def divide_students(students):
    groups = [[], []]
    for index, student in enumerate(students):
        if index %2 == 0:
            groups[0].append(student)
        else:
            groups[1].append(student)
    return(groups)

#kendime not
#burada 2 listeli bir liste oluşturmayı unutmamalıyım
#ve append ederken indekse göre append edebileceğimi hatırlamalıyım

students = ["John", "Mark", "Venessa", "Mariam"]

divide_students(students)
