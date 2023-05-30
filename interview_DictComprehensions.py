#Amaç: çift sayıların karesi alınarak bir sözlüğe eklenecek

numbers = range(10)

new_dict = {}

for n in numbers:
    if n %2 == 0:
    new_dict[n] = n ** 2

new_dict

#asıl amaç daha kısa olması=dict comprehension

{n: n ** 2 for n in numbers if n %2 == 0}