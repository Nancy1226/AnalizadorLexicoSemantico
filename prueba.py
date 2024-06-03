import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt

datasetData = pd.read_excel('221201.csv')

listaValores = []
listaPadres= []
listaAptitud = []
listaMejorY = []


for index, row in datasetData.iterrows():
    # Extraer los valores de las columnas para esta fila
    x1 = row['x1']
    x2 = row['x2']
    x3 = row['x3']
    x4 = row['x4']
    y = row['y']
    listaValores.append([x1, x2, x3, x4, y, index+1])

def ordenarMejoresY(listaY):
    listaOrdenada = sorted(listaY, key=lambda x: abs(x[3]))

    return listaOrdenada[0]

def graficarMejoresY(listaValores):

    print("Imprimiendo la listaValores")
    print(listaValores)

    generaciones = sorted(set(individuo[5] for individuo in listaValores))

    if listaValores: 
        # Inicializar listas para los valores de Mejor, Promedio y Peor
        yCalculada = []
        yDefinida = []

        # Recorremos la lista en bloques de 3 (Mejor, Promedio, Peor)
        for i in range(0, len(listaValores), 1):
            yCalculada.append(listaValores[i][1])
            yDefinida.append(listaValores[i][2])
    else:
        generaciones = []
        yCalculada = []
        yDefinida = []
    
    plt.plot(generaciones, yCalculada, color='red', linestyle='-', label='Y calculada')
    plt.plot(generaciones, yDefinida, color='blue', linestyle='-', label='Y definida')

    plt.grid()
    plt.xlabel('Generación')
    plt.ylabel('Y')
    plt.title('Comparativa de Y.')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(f'Evolución_Y.png',  bbox_inches='tight')
    plt.close()



def graficar_y_guardar(listaAptitud):

    #Ordenamos las generaciones por su generación
    generaciones = sorted(set(individuo[5] for individuo in listaAptitud))

    if listaAptitud: 
        # Inicializar listas para los valores de Mejor, Promedio y Peor
        mejores = []
        promedios = []
        peores = []

        # Recorremos la lista en bloques de 3 (Mejor, Promedio, Peor)
        for i in range(0, len(listaAptitud), 3):
            mejores.append(listaAptitud[i][1])
            promedios.append(listaAptitud[i+1][1])
            peores.append(listaAptitud[i+2][1])
    else:
        generaciones = []
        mejores = []
        promedios = []
        peores = []
    
    # Crear la gráfica

    plt.plot(generaciones, mejores, color='c', linestyle='-', label='Mejor')
    plt.plot(generaciones, promedios, color='darkcyan', linestyle='-', label='Promedio')
    plt.plot(generaciones, peores, color='indigo',  linestyle='-', label='Peor')

    plt.grid()
    plt.xlabel('Generación')
    plt.ylabel('Y Calculada')
    plt.title('Evolución de la Aptitud por Generación.')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(f'Evolución_Aptitud.png',  bbox_inches='tight')
    plt.close()


def filtroAptitud(listaFiltrada):
    if not listaFiltrada:
        return None, None, None
    
    # Ordenar la lista en función de Fx
    listaOrdenada = sorted(listaFiltrada, key=lambda x: abs(x[3]))
    
    # Obtener el mejor, peor y promedio
    mejor = listaOrdenada[0]
    mejor_con_generacion = list(mejor) + ["Mejor"]
    peor = listaOrdenada[-1]
    peor_con_generacion = list(peor) + ["Peor"]
    promedio = listaOrdenada[len(listaOrdenada) // 2]
    promedio_con_generacion = list(promedio) + ["Promedio"]
    
    return [mejor_con_generacion, promedio_con_generacion, peor_con_generacion]


def poda(listaFx, cantidadPoda):
    global listaPadres
    listaPadres.clear()

    ordenada = sorted(listaFx, key=lambda x: abs(x[3]))

    podada = []
    for elemento in ordenada:
        if elemento not in podada:
            podada.append(elemento)
            if len(podada) == cantidadPoda:
                break

    listaPadres = list(podada)

def calcularFx(individuos, generacion):
    global listaValores

    resultado = []
    for individuo in individuos:
        for valores in listaValores:
            x1, x2, x3, x4, y, fila = valores
            yCalculada = individuo[0] + (individuo[1] * x1) + (individuo[2] * x2) + (individuo[3] * x3) + (individuo[4] * x4)
            yCalculadaRounded = round(yCalculada, 2)
            margen = yCalculadaRounded - y
            margenRounded = round(margen, 2)
            resultado.append([individuo, yCalculadaRounded, y, abs(margenRounded), fila, generacion])
    return resultado
    


def mutacion(hijos, rango_mutacion):
    mutados = []
    for hijo in hijos:
        mutante = hijo[:]  # Crear una copia del individuo
        for i in range(len(mutante)):
            if random.random() <= rango_mutacion:
                #mutante[i] = random.randint(-100, 100)
                mutante[i] = mutante[i] * (1 + random.randint(-1, 1)) #así como lo quiere el doc
        mutados.append(mutante)
    return mutados


def cruzaParejas(parejas):
    hijos = []
    for pareja in parejas:
        padre1, padre2 = pareja
        punto_cruce = random.randint(1, len(padre1) - 1)
        print(f"Punto de cruza: {punto_cruce}")
        hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
        hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
        hijos.extend([hijo1, hijo2])
    return hijos

def crearParejas(poblacion, probabilidad_parejas):
    parejas = []
    indices = list(range(len(poblacion)))
    random.shuffle(indices)  # Mezclar los índices aleatoriamente
    for i in range(0, len(poblacion), 2):
        if random.random() <= probabilidad_parejas:
            # Formar una pareja con los individuos en las posiciones i e i+1
            pareja = [poblacion[indices[i]], poblacion[indices[i+1]]]
            parejas.append(pareja)
            print("Se creo la pareja ")
        else: print("No cumplio con la probablidad")
    return parejas

def crear_poblacion(tamano_poblacion):
    poblacion = []
    for i in range(tamano_poblacion):
        individuo = [random.randint(-100, 100) for j in range(5)]  # Generar valores aleatorios para A, B, C, D, E
        poblacion.append(individuo)
    return poblacion

def procesarDatos():
    global listaPadres, listaAptitud, listaMejorY

    if listaPadres:
        listaPadres.clear()
        print("La lista padres ha sido limpiada.")

    if listaAptitud:
        listaAptitud.clear()
        print("La lista aptitud ha sido limpiada.")

    if listaMejorY:
        listaMejorY.clear()
        print("La listaMejorY ha sido limpiada.")

    tamano_poblacion = int(input("Ingrese la población: "))
    generaciones = int(input("Ingrese el número de generaciones: "))
    probabilidad_parejas = float(input("Ingrese la probabilidad de parejas (entre 0 y 1): "))
    probabilidad_mutacion = float(input("Ingrese la probabilidad de mutación (entre 0 y 1): "))
    cantidad_poda = int(input("Ingrese los individuos que quedaran en la poda: "))

    poblacion = crear_poblacion(tamano_poblacion)

    print("la poblacion es: ")
    print(poblacion)

    for indice in range(generaciones):
        nueva_poblacion = []
        nueva_poblacion = list(listaPadres)

        if listaPadres and len(listaPadres) > 0 and len(listaPadres[0]) > 0:
            listaValoresPos0 = [padre[0] for padre in listaPadres]
            parejasCreadas = crearParejas(listaValoresPos0, probabilidad_parejas)
        else:
            parejasCreadas = crearParejas(poblacion, probabilidad_parejas)

        print(f"imprimiendo listaPadres en la generacion {indice +1 }")
        for padres in listaPadres:
            print(padres)
       
        
        hijos = cruzaParejas(parejasCreadas)
        
        mutados = mutacion(hijos, probabilidad_mutacion)

        nueva_poblacion.extend(mutados)

        listaFX = calcularFx(mutados, indice)

        mejorGeneracion = ordenarMejoresY(listaFX)

        print("El mejor de la generacion")
        print(mejorGeneracion)

        listaMejorY.append(mejorGeneracion)

        graficarMejoresY(listaMejorY)

        listaFiltro = filtroAptitud(listaFX)

        listaAptitud.extend(listaFiltro)

        poda(listaFX, cantidad_poda)

        print("Imprimiendo la lista de los mejores: ")
        for mejores in listaAptitud:
            print(mejores)

        graficar_y_guardar(listaAptitud)
        
        
procesarDatos()
