# import pandas as pd
import copy
import random
import math

from classes.ClientData import ClientData
from classes.Individual import Individual

CAPACITY = 0
N_CLIENTS = 0
NUMBER_OF_GENES =0
NUMBER_OF_ORGANISMS = 100
MAX_GENERATION_NUMBER = 1000
MUTATION_RATE= 0.001

def read_file(file_location_path):
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

def initialize_organisms(depot_data, clients_data):
    organisms = []
    for _ in range(NUMBER_OF_ORGANISMS):
        organisms.append(
            Individual(depot_data, clients_data, CAPACITY)
        )
    return organisms

def evaluate_organisms(organisms, origin, client):
    best_fitness = 0
    for org_index in range(NUMBER_OF_ORGANISMS):
        ##EVALUATE ROUTE
        path_cost = evaluate_path( organisms[org_index]["genes"], origin , client )
        organisms[org_index]["fitness"] = path_cost
        if(path_cost < best_fitness):
            best_fitness = path_cost
    return best_fitness

def get_total_fitness(orgs):
    total_fitness = 0 
    for fitness in [ org["fitness"] for org in  orgs]:
        total_fitness += fitness
    return total_fitness

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
    orgs = initialize_organisms(clients)
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
    initialize_organisms(depot_data, clients_data)
    #final_generation = nsga2_main_loop( depot_data,  clients_data)
    #print(orgs[0])
main()

### Inicializar
### Clasificar en frentes 
### Seleccion de sgte. poblacion
### Criterio de parada ( Nro. de generaciones - Que no cambien los frentes x n generaciones )