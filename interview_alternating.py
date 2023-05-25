#Avrupadaki bir üniversitenin bilgisayar bilimleri departmanına alınacak doktora öğrencisi için sorulan sorulardan biri

#Amaç: aşağıdaki şekilde string değiştiren fonksiyon yazdırmak istiyoruz
#(girilen string ifadeleri çift indeksleri büyült, tek indekslileri küçült)

#before: "hi my name is john and i am leraning python"
#after:"Hi My NaMe iS JoHn aNd i aM LeArNiNg pYtHoN"

def alternating(string):
    new_string = ""
    #girilen stringin indekslerinde gez
    for string_index in range(len(string)):
        #indeks çift ise büyük harfe çevir
        if string_index %2 == 0:
            new_string += string[string_index].upper()
        #indeks tek ise küçük harfe çevir
        else:
            new_string += string[string_index].lower()
    print(new_string)


alternating("hi my name is john and i am leraning python")


#solution2
#alternating fonksiyonunun enumerate ile yazılması

def alternating_with_enumerate(string):
    new_string =""
    for index, letter in enumerate(string):
        if index %2 == 0:
            new_string += letter.upper()
        else:
            new_string += letter.lower()
    return(new_string)

alternating_with_enumerate("günaydın")

#not: kod okunabilirliği açısından ve takip edilebilmesi açısından daha iyi bir yöntem