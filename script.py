# import pandas as pd
import copy
from os import pardir
import random
import math

from clases.ClientData import ClientData
from clases.Individual import Individual

# los tres primeros datos serán cargados al leer el archivo
CAPACITY = 0
N_CLIENTS = 0
NUMBER_OF_GENES =0
NUMERO_DE_INDIVIDUOS = 100
MAX_GENERATION_NUMBER = 1000
PROPORCION_ELITISTA = 0.1
PROPORCION_CROSSOVER = 0.9
PROPORCION_MUTACION = 0.05 
MUTATION_RATE= 0.04
# variable global diccionario para mapear individuos a sus indices
dict_individual_number = {}

def read_file(file_location_path):
# función para leer el archivo y procesar para que pueda ser utilizado
    clients_data = []
    with open(file_location_path) as data:
        for i, line in enumerate(data):
            global CAPACITY
            global N_CLIENTS
            global NUMBER_OF_GENES
            if i == 1: 
                N_CLIENTS = int(line) - 1
                NUMBER_OF_GENES = int(line) - 1
            if i == 3: CAPACITY = int(line)
            if i > 4:
                cols = line.split()
                clients_data.append(ClientData(
                    client_number = int(cols[0]), 
                    x = int(cols[1]), 
                    y = int(cols[2]), 
                    demand = int(cols[3]),
                    ready_time = int(cols[4]),
                    due_date = int(cols[5]),
                    service_time = int(cols[6])
                ))
    return clients_data;

def inicializar_poblacion(depot_data, clients_data):
# función que instancia todos los individuos de la población
    poblacion = []
    for _ in range(NUMERO_DE_INDIVIDUOS):
        poblacion.append(
            Individual(depot_data, clients_data, CAPACITY)
        )
    return poblacion

def ranking_de_frentes(poblacion):
# función que se encarga de clasificar a toda la población en frentes pareto y en base a eso asignarles un dummy fitness
    front = 0
    poblacion_actual = poblacion
    poblacion_en_frentes = []
    # mientras todos los individuos no pertenezcan a un frente
    while(poblacion_no_clasificada(poblacion_actual, poblacion_en_frentes)):
        # se creará un nuevo frente pareto para clasificar individuos
        front+= 1
        # calculamos un nuevo frente
        nuevo_frente, poblacion_actual = calcular_frente(poblacion_actual, front)
        # print('frente {}'.format(front))
        # for ind in nuevo_frente:
        #     print(dict_individual_number[ind])
        poblacion_en_frentes.append( nuevo_frente )
    
def poblacion_no_clasificada(poblacion, poblacion_en_frentes):
# mientras los individuos en un frente pareto sean < que la población total significa que no se han clasificado todos los individuos
    # print('termina? {}'.format(not(len(poblacion) > len(poblacion_en_frentes))))
    return len(poblacion) > len(poblacion_en_frentes)

def calcular_frente(poblacion_actual, front):
# función que calcula el frente pareto de la población actual
    nuevo_frente = []
    for individuo in poblacion_actual:
        es_dominado = False
        for individuo_comp in poblacion_actual:
            # si algun elemento es mejor (menor por ser minimización) en ambos fitness objetivo entonces este individuo es dominado
            if (individuo_comp.cantidad_vehiculos < individuo.cantidad_vehiculos and individuo_comp.tiempo_total_vehiculos < individuo.tiempo_total_vehiculos):
                es_dominado = True 
        # si el individuo es no dominado
        if es_dominado == False:
            # lo asignamos al frente pareto
            nuevo_frente.append(individuo)
            # luego calculamos su fitness
            individuo.calcular_fitness_final(front ,nuevo_frente) # también debemos hacer la degradación de nicho
    # quitamos los elementos de la poblacion actual que ya están en el frente
    poblacion_actual = [item for item in poblacion_actual if item not in nuevo_frente]

    return nuevo_frente, poblacion_actual

def verificar_si_domina(individuo, individuo_comp):
# función para verificar si un individuo domina sobre otro (funcion en desuso)
    domina = False
    indcv = individuo.cantidad_vehiculos    
    indtv = individuo.tiempo_total_vehiculos
    iccv = individuo_comp.cantidad_vehiculos
    ictv = individuo_comp.tiempo_total_vehiculos
    if (indcv <= iccv and indtv <= ictv ):
        if (indcv < iccv or indtv < ictv):
            domina = True ;
        else:
            domina = False;
    return domina

def dibujar_frente_pareto(poblacion):
# función para graficar el frente pareto teniendo como eje x a F1(cant vehiculos) y como eje y a F2(tiempo total vehiculos)
# Para guardar el gráfico, llamar solo a esta función en main y ejecutamos el comando: python script.py > matriz.txt
    # inicializamos la matriz
    matriz = [[' ' for col in range(100)] for row in range(100)]
    # recorremos todos los individuos de la población
    for i in range(0,len(poblacion)):
        cant_vehiculos = poblacion[i].get_fitness_objetivos()[0]
        tiempo_total = poblacion[i].get_fitness_objetivos()[1]
        # convertimos el rango [21000,27000] a [0,100]
        tiempo_total = int (((tiempo_total - 20000)/(30000 -21000) ) * 100)
        # ahora cargamos en la matriz
        matriz[cant_vehiculos][tiempo_total] = i
        # guardamos en el diccionario para poder saber que individuo entró en cada frente
        dict_individual_number[poblacion[i]] = i
    # por último imprimimos el gráfico
    # aclaración: esta impresión hace que la Y sea la F1 y la X la F2
    for i in range(100):
        print(" {}".format(matriz[i]))
    print("\n")

def ordenar_poblacion_por_fitness(poblacion):
#ordenamos la población según el fitness final calculado
    poblacion.sort(key= lambda individual: individual.fitness, reverse= True)

def seleccion_elitista(poblacion):
# elegimos de manera elitista al 10% mejor de la población para que pase a la siguiente generación
    # cant is the amount of elements of the population to be select with elistism
    cant = int(NUMERO_DE_INDIVIDUOS*PROPORCION_ELITISTA)
    # we select the 'cant' amount of elements and append to the sucesors list
    siguiente_generacion = []
    for ind in range(0,cant):
        siguiente_generacion.append(poblacion[ind])
    
    return siguiente_generacion

def mutacion(poblacion):
# función que agarra a la población de la nueva generación y tiene cierta probabilidad de mutar algunos de sus genes
    # first we calculate the amount of elements to be mutated
    cant = math.ceil(PROPORCION_MUTACION * len(poblacion))
    # then we choose those elements
    for i in range(0,cant):
        indiv = random.choice(poblacion)
        # for each element we mutate every gene with a probability of 0.04
        size = len(indiv.get_ruta())
        for g in range(size):
            if( random.random() <= MUTATION_RATE ):
                # if there will be a mutation we choose another gen index and we swap both
                swap = random.randint(0,size-1)
                while swap == g:
                    swap = random.randint(0,size-1)
                # print(indiv[g],indiv[swap])
                # DEBO COMPROBAR QUE EN LA POBLACIÓN FINAL ESTÉN LOS INDIVIDUOS MUTADOS !!!!!!!!
                indiv.get_ruta()[g],indiv.get_ruta()[swap] = indiv.get_ruta()[swap],indiv.get_ruta()[g]

def reproduccion_crossover(poblacion):
# función que realiza la reproducción de individuos mediante crossover. Previamente elige cada par con la ruleta
    # next_generation = copy.deepcopy(organisms)
    nueva_generacion = []
    # repetir mientras el tamaño de la nueva generación sea menor a la proporcion de sucesores que debe generar el crossover
    while(len(nueva_generacion) < ( NUMERO_DE_INDIVIDUOS * PROPORCION_CROSSOVER)):
        # elegimos un padre y una madre con la técnica de la ruleta
        padre = get_parent_usando_ruleta(poblacion)
        madre = get_parent_usando_ruleta(poblacion)
        break
    return nueva_generacion

def get_parent_usando_ruleta(poblacion):
# función para obtener un padre con la técnica de la ruleta para aplicar la reproducción
    # obtenemos la suma total de fitness de todos los individuos
    total_fitness = int(get_total_fitness(poblacion))
    # elegimos un punto random que será el individuo a elegir
    random_select_point = random.randint(1,total_fitness)
    sumatoria_actual = 0
    for i in range(NUMERO_DE_INDIVIDUOS):
        # vamos sumando los valores de fitness
        sumatoria_actual += poblacion[i].fitness
        #hasta llegar o superar al punto random elegido entonces retornamos el individuo que llegó a ese punto
        if sumatoria_actual >= random_select_point:
            return poblacion[i]

def get_total_fitness(poblacion):
# función que retorna la sumatoria de fitness de toda la población
    total_fitness = 0
    for individuo in poblacion:
        total_fitness += individuo.fitness
    return total_fitness

def get_avg_from_orgs(orgs):
    return get_total_fitness(orgs) / NUMERO_DE_INDIVIDUOS

def get_best_from_orgs(orgs):
    best = orgs[0]
    for i in range(NUMERO_DE_INDIVIDUOS):
        if( orgs[i]["fitness"] > best["fitness"] ):
            best = orgs[i]
    return best

def nsga(poblacion):
# función que realiza el ciclo o la generación de la población según el método MOEA NSGA
    # VERIFICAR QUE LA POBLACIÓN VAYA PASANDO ENTRE FUNCIONES POR REFERENCIA O CAMBIAR A POR VALOR !!!!!!!!
    generacion = 1
    # mientras no se cumpla la condición de parada. Cada ciclo del while es una generación
    while(not condicion_parada(generacion)):
        # realizamos el ranking de frentes para clasificar a la población y darles un fitness
        ranking_de_frentes(poblacion)
        # ordenamos a la población de acuerdo a su fitness
        ordenar_poblacion_por_fitness(poblacion)
        # Mostramos al mejor individuo de la generación actual
        print('generacion {}: Mejor individuo = Fitness: {}, cant vehiculos: {}, tiempo total: {}'.format(generacion,poblacion[0].fitness,poblacion[0].cantidad_vehiculos,poblacion[0].tiempo_total_vehiculos))
        # procedemos a la selección y reproducción:
        nueva_generacion = []
        # primero elegimos a los mejores de la generación actual y los hacemos pasar a la nueva generación
        nueva_generacion = seleccion_elitista(poblacion)
        # luego realizamos crossover para completar los individuos de la nueva generación
        nueva_generacion += reproduccion_crossover(poblacion)
        # por último mutamos con cierta probabilidad un porcentaje de la nueva población
        mutacion(nueva_generacion)
        # luego incrementamos el número de generación
        generacion += 1
        
    # finalmente mostramos al mejor individuo final
    print('generacion {} (FINAL): Mejor individuo = Fitness: {}, cant vehiculos: {}, tiempo total: {}'.format(generacion-1,poblacion[0].fitness,poblacion[0].cantidad_vehiculos,poblacion[0].tiempo_total_vehiculos))

def condicion_parada(generacion):
# función donde pondremos las condiciones para que el ciclo NSGA se detenga
    parada = False
    # primera condición: cantidad de iteraciones
    if (generacion > MAX_GENERATION_NUMBER):
        parada = True
    return parada


def main():
    data = read_file("vrptw_c101.txt");
    clients_data = data[1:]
    depot_data = data[0]
    poblacion = inicializar_poblacion(depot_data, clients_data)
    
    # dibujar_frente_pareto(poblacion)

    nsga(poblacion)

    # for individuo in poblacion:
    #     print('individuo:')
    #     print(individuo.fitness)
    #     # get_fitness_objetivos retorna el valor de las funciones objetivo
    #     print(individuo.get_fitness_objetivos())
    #     print(individuo.get_ruta())

main()

### Inicializar
### Clasificar en frentes 
### Seleccion de sgte. poblacion
### Criterio de parada ( Nro. de generaciones - Que no cambien los frentes x n generaciones )