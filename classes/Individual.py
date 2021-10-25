import copy
import random
import math

class Individual(object):
    def generate_random_individual(self):
        clients_to_visit = copy.deepcopy(self.clients_data)
        path = []
        while clients_to_visit:
            index = random.randint(0, len(clients_to_visit))
            if index == len(clients_to_visit): #Adding a truck!
                path.append(0)
            else: #Adding valid values
                path.append( clients_to_visit[index].client_number )
                del clients_to_visit[index]

        self.genes = path # Genes is an array with the client_number of the clients_data vector
        self.fitness = 0

    def heuristic_repair(self):
        new_genes_valid_capacity = []
        total_cargo = 0
        for client_number in self.genes:
            if client_number == 0:
                total_cargo = 0 # If we go to depot, we just dont do anything
            else:#If we have a client with a demand
                position = self.clients_data[ client_number - 1]
                total_cargo += position.demand # Load the cargo with the demand
                if total_cargo >= self.max_capacity: #If the cargo is greater than the max
                    new_genes_valid_capacity.append(0) #Add new truck here
                    total_cargo = position.demand # THe new truck will have a new capacity
                #If not, just continue the visit of the next client
                new_genes_valid_capacity.append(client_number)
        
        #With the logic above new_genes has valid travels for many trucks that doesnt violate the capacity restriction
        #Now we have to repair the time windows
        
        new_genes_valid_time = []
        time = 0
        position = self.depot_data
        for client_number in new_genes_valid_capacity:
            if client_number == 0:
                time = 0# Restart time because this is a new truck
                position = self.depot_data
            else:
                client_to_serve = self.clients_data[ client_number - 1 ]
                time +=  position.get_distance_to_client( client_to_serve )
                if client_to_serve.can_serve_in_timepoint(time):
                    position = client_to_serve
                    if client_to_serve.timepoint_is_before(time): # si llegamos antes, esperamos....
                        time = client_to_serve.ready_time + client_to_serve.service_time 
                    else:
                        time += client_to_serve.service_time#if we arrive on time we just add the time
                else:
                    new_genes_valid_time.append(0) # Add new truck
                    time = client_to_serve.ready_time + client_to_serve.service_time # Restart time because this is a new truck
                new_genes_valid_time.append(client_number)
        
        self.genes = new_genes_valid_time

    def __init__(self, depot_data, clients_data, max_capacity):
        self.clients_data = clients_data
        self.depot_data = depot_data
        self.max_capacity = max_capacity
        self.generate_random_individual()
        self.heuristic_repair()