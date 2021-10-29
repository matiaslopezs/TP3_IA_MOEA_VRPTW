# import pandas as pd
import copy
import random
import math

from clases.ClientData import ClientData
from clases.Individual import Individual

# los tres primeros datos serán cargados al leer el archivo
CAPACITY = 0
N_CLIENTS = 0
NUMBER_OF_GENES =0
NUMBER_OF_ORGANISMS = 100
MAX_GENERATION_NUMBER = 1000
MUTATION_RATE= 0.001

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
    for _ in range(NUMBER_OF_ORGANISMS):
        poblacion.append(
            Individual(depot_data, clients_data, CAPACITY)
        )
    return poblacion

##################### ESTAS FUNCIONES POSIBLEMENTE NO USE Y DEBA BORRAR #######################
def evaluate_organisms(organisms, origin, client):
    best_fitness = 0
    for org_index in range(NUMBER_OF_ORGANISMS):
        ##EVALUATE ROUTE
        path_cost = evaluate_path( organisms[org_index]["genes"], origin , client )
        organisms[org_index]["fitness"] = path_cost
        if(path_cost < best_fitness):
            best_fitness = path_cost
    return best_fitness

def evaluate_path(gene, origin, client):
    None

def get_total_fitness(orgs):
    total_fitness = 0 
    for fitness in [ org["fitness"] for org in  orgs]:
        total_fitness += fitness
    return total_fitness

##################### HASTA ACÁ #######################

def ranking_de_frentes(poblacion):
# función que se encarga de clasificar a toda la población en frentes pareto y en base a eso asignarles un dummy fitness
    front = 0
    poblacion_actual = poblacion
    poblacion_en_frentes = []
    # mientras todos los individuos no pertenezcan a un frente
    while(poblacion_no_clasificada(poblacion, poblacion_en_frentes)):
        # se creará un nuevo frente pareto para clasificar individuos
        front+= 1
        # calculamos un nuevo frente
        # POBLACIÓN ACTUAL NO ESTÁ SIENDO ACTUALIZADA, SOLO CAMBIA SU VALOR DENTRO DE CALCULAR FRENTE PERO ESO NO SE RETORNA !!!!
        poblacion_en_frentes.append( calcular_frente(poblacion_actual, front) )

def poblacion_no_clasificada(poblacion, poblacion_en_frentes):
# mientras los individuos en un frente pareto sean < que la población total significa que no se han clasificado todos los individuos
    return len(poblacion) > len(poblacion_en_frentes)

def calcular_frente(poblacion_actual, front):
# función que calcula el frente pareto de la población actual
    nuevo_frente = []
    for individuo in poblacion_actual:
        band = 0
        for individuo_comp in poblacion_actual:
            # si algun elemento es mejor (menor por ser minimización) en ambos fitness objetivo entonces este individuo es dominado
            if (individuo_comp.cantidad_vehiculos < individuo.cantidad_vehiculos and individuo_comp.tiempo_total_vehiculos < individuo.tiempo_total_vehiculos):
                band = 1 
        # si el individuo es no dominado
        if band == 0:
            # lo quitamos de la población actual
            poblacion_actual.remove(individuo)
            # lo asignamos al frente pareto
            nuevo_frente.append(individuo)
            # luego calculamos su fitness
            # IMPLEMENTAR FUNCION CALCULAR FITNESS!!!!!!!!!!
            individuo.calcular_fitness(front ,nuevo_frente) # también debemos hacer la degradación de nicho
    
    return nuevo_frente

def dibujar_frente_pareto(poblacion):
# función para graficar el frente pareto teniendo como eje x a F1(cant vehiculos) y como eje y a F2(tiempo total vehiculos)
    # inicializamos la matriz
    matriz = [[' ' for col in range(100)] for row in range(100)]
    # recorremos todos los individuos de la población
    for i in range(0,len(poblacion)):
        cant_vehiculos = poblacion[i].get_fitness()[0]
        tiempo_total = poblacion[i].get_fitness()[1]
        # convertimos el rango [21000,27000] a [0,100]
        tiempo_total = int (((tiempo_total - 21000)/(27000 -21000) ) * 100)
        # ahora cargamos en la matriz
        matriz[cant_vehiculos][tiempo_total] = i
    # por último imprimimos el gráfico
    # aclaración: esta impresión hace que la Y sea la F1 y la X la F2
    for i in range(100):
        print(" {}".format(matriz[i]))
    print("\n")


def get_parent_using_roulette(organisms):
    total_fitness = get_total_fitness(organisms)
    random_select_point = random.randint(1,total_fitness)
    running_total = 0
    for i in range(NUMBER_OF_ORGANISMS):
        running_total += organisms[i]["fitness"]
        if running_total >= random_select_point:
            return organisms[i]

def produce_next_generation(organisms):
    next_generation = copy.deepcopy(organisms)
    for org_index in range(NUMBER_OF_ORGANISMS):
        dad = get_parent_using_roulette(organisms)
        mom = get_parent_using_roulette(organisms)
        crossover_point = random.randint(0, NUMBER_OF_GENES)
        for j in range(NUMBER_OF_GENES):
            is_a_mutation = random.randint( 1,int(1/MUTATION_RATE) )
            if(is_a_mutation == 1): #        // we decided to make this gene a mutation
                next_generation[org_index]["genes"][j] = random.randint(1,9)
            else:
                #// we decided to copy this gene from a parent
                if j < crossover_point:
                    next_generation[org_index]["genes"][j] = dad[j]
                else:
                    next_generation[org_index]["genes"][j] = mom[j]
    return next_generation

def get_avg_from_orgs(orgs):
    return get_total_fitness(orgs) / NUMBER_OF_ORGANISMS

def get_best_from_orgs(orgs):
    best = orgs[0]
    for i in range(NUMBER_OF_ORGANISMS):
        if( orgs[i]["fitness"] > best["fitness"] ):
            best = orgs[i]
    return best

def nsga2_main_loop( origin, clients ):
    #Create a combined population with parents and sibblings
        #Create roulette and generate sibblings
    #Rank and sort the created set with the performance on defined target indicators
        #Sort using domination: get a list for every solution that list should contain
        #which solutions are dominated by the current solution and we should also
        #have a counter of how many solutions dominate the current one

        #once we have that set, all the solutions that arent dominated by any other
        #are the rank1 - Front1, then all the ones that are dominated just by
        #Front1 solutions are front2, and you make that iteration over and over again

    #Take best members and create new population 
        #We take solutions(individuals) from the 3 first fronts(ranks) and to fill up the
        #rest we us CROWDING DISTANCE SORTIG:  
    
    ##THIS BELOW IS AN EASIER IMPLEMENTATION TO USE MEANWHILE
    generation_count = 0
    orgs = inicializar_poblacion(clients)
    while( generation_count < MAX_GENERATION_NUMBER ):
        perfect_generation = evaluate_organisms(orgs, origin, clients)
        best = get_best_from_orgs(orgs)
        print ("{:<8} {:<20} {:<15} {:<15}".format(generation_count, get_total_fitness(orgs), get_avg_from_orgs(orgs), best["fitness"] ), best["genes"] )
        orgs = produce_next_generation(orgs)
        generation_count+=1

def main():
    data = read_file("vrptw_c101.txt");
    clients_data = data[1:]
    depot_data = data[0]
    poblacion = inicializar_poblacion(depot_data, clients_data)
    
    # dibujar_frente_pareto(poblacion)
    
    for individuo in poblacion:
        print(individuo.get_fitness())
        # print(individuo.get_ruta())
    
    #final_generation = nsga2_main_loop( depot_data,  clients_data)
    #print(orgs[0])

main()

### Inicializar
### Clasificar en frentes 
### Seleccion de sgte. poblacion
### Criterio de parada ( Nro. de generaciones - Que no cambien los frentes x n generaciones )