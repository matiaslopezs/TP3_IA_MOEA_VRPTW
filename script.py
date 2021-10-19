# import pandas as pd
import copy
import random
import math

from classes import ClientData
CAPACITY = 0
N_CLIENTS = 0
NUMBER_OF_GENES =0
NUMBER_OF_ORGANISMS = 100
MAX_GENERATION_NUMBER = 100
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
                # clients_data.append(ClientData(int(cols[0]), int(cols[1]), int(cols[2]), int(cols[3]),
                #     int(cols[4]),int(cols[5]),int(cols[6])
                # ))
                clients_data.append({
                    "client_number": int(cols[0]),
                    "x": int(cols[1]),
                    "y": int(cols[2]),
                    "demand": int(cols[3]),
                    "ready_time": int(cols[4]),
                    "due_date": int(cols[5]),
                    "service_time": int(cols[6])
                });
    return clients_data;

def initializeOrganisms(clients_data):
    organisms = []
    for _ in range(NUMBER_OF_ORGANISMS):
        clients_to_visit = copy.deepcopy(clients_data)
        path = []
        while clients_to_visit:
            index = random.randint(0, len(clients_to_visit) -1)
            path.append( clients_to_visit[index]['client_number'] )
            del clients_to_visit[index]
        organisms.append({
            "genes": path,
            "fitness": 0,
        })
    return organisms

def get_distance(p1, p2):
    return math.dist( [p1['x'], p1['y']], [p2['x'], p2['y']] )

def evaluate_path(path, origin):
    total_cost = 0
    position = origin
    total_cargo = 0
    for i in range( len(path) ):
        total_cargo += path[i]["demand"]
        if total_cargo >= CAPACITY:
            total_cost += get_distance(position, origin)# Go back to origin to empty cargo
            total_cost += get_distance(origin, position) # Go to the client that we must serve
            total_cargo = path[i]["demand"] # The cargo is now just the demand of the current client
        else:
            total_cost += get_distance( position, path[i] )
        position = path[i]
    return total_cost

def evaluate_organisms(organisms, origin):
    total_fitness = 0
    best_fitness = 0
    for org_index in range(NUMBER_OF_ORGANISMS):
        ##EVALUATE ROUTE
        path_cost = evaluate_path( organisms[org_index]["genes"], origin )
        organisms[org_index]["fitness"] = path_cost
        total_fitness += path_cost

        if(path_cost > best_fitness):
            best_fitness = path_cost
    return best_fitness

def produce_next_generation(organisms):
    nextGeneration = copy.deepcopy(organisms)
    

def nsga2_main_loop():
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
    pass
def main():
    data = read_file("vrptw_c101.txt");
    clients_data = data[1:]
    depot_data = data[0]
    orgs = initializeOrganisms(clients_data)
    print(orgs[0])
main()