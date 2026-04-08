palos=["oro","copa","espada","basto"]
numeros=[1,2,3,4,5,6,7,10,11,12]

def valor_truco(numero,palo):
    if numero==1 and palo=="espada":
        return 14
    elif numero==1 and palo=="basto":
        return 13
    elif numero==7 and palo=="espada":
        return 12
    elif numero==7 and palo=="oro":
        return 11
    elif numero==3:
        return 10
    elif numero==2:
        return 9
    elif numero==1 and (palo=="oro" or palo=="copa"):
        return 8
    elif numero==12:
        return 7
    elif numero==11:
        return 6
    elif numero==10:
        return 5
    elif numero==7:
        return 4
    elif numero==6:
        return 3
    elif numero==5:
        return 2
    elif numero==4:
        return 1
    
mazo=[]

for palo in palos:
    for numero in numeros:
        carta=[numero,palo,valor_truco(numero,palo)]
        mazo.append(carta)

print("Mazo:")
for carta in mazo:
    print(carta)