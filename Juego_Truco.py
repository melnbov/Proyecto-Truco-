def elegirpuntos():
    puntos=int(input("Desea que la partida se defina a los 15 o 30 puntos? Escriba el numero: "))
    while puntos != 15 and puntos != 30:
        puntos=int(input("Valor invalido, ingraese 15 o 30: "))
    return puntos

puntosmax= elegirpuntos()
print("El partido se jugara a", puntosmax, "puntos")