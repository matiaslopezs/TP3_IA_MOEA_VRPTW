import copy
import random
import math

class Individual(object):

    def generate_random_individual(self):
        # función que genera individuos aleatorios
        clients_to_visit = copy.deepcopy(self.clients_data)
        path = []
        while clients_to_visit:
            # mientras hayan clientes en la lista a visitar, se elige un cliente random
            index = random.randint(0, len(clients_to_visit)-1)
            # if index == len(clients_to_visit): #Adding a truck!
            #     path.append(0)
            # else: #Adding valid values
            # y se guarda el cliente random en la lista path
            path.append( clients_to_visit[index].client_number )
            # luego se borra al cliente de la lista original
            del clients_to_visit[index]

        #guardamos path en el array genes, será un array de números que simbolizan el número del cliente.
        self.genes = path # Genes is an array with the client_number of the clients_data vector
        self.fitness = 0

    def heuristic_repair_and_fitness(self):
    # este algoritmo realiza la reparación heurísitca y al mismo tiempo calcula el fitness con las variables globales:
    # self.cantidad_vehiculos y self.tiempo_total_vehiculos.
        new_genes_valid_capacity = []
        total_cargo = 0
        for client_number in self.genes:
            position = self.clients_data[ client_number - 1]
            total_cargo += position.demand # Load the cargo with the demand
            if total_cargo >= self.max_capacity: #If the cargo is greater than the max
                new_genes_valid_capacity.append(0) #Add new truck here
                self.cantidad_vehiculos+=1 # se añade un vehículo a la cantidad
                # si el otro camión se llenó entonces le ponemos a este la carga desde el punto
                # por eso se inicializa de nuevo total_cargo a ese valor
                total_cargo = position.demand # THe new truck will have a new capacity
        #     #If not, just continue the visit of the next client
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
                
                # Sumamos primero al tiempo total el tiempo en llegar del punto actual al destino
                self.tiempo_total_vehiculos += position.get_distance_to_client( client_to_serve ) 

                if client_to_serve.can_serve_in_timepoint(time):
                    position = client_to_serve
                    if client_to_serve.timepoint_is_before(time): # si llegamos antes, esperamos....
                        
                        # si debe esperar entonces se carga el tiempo de espera + el tiempo de servicio
                        self.tiempo_total_vehiculos += (client_to_serve.ready_time - time) + client_to_serve.service_time 

                        time = client_to_serve.ready_time + client_to_serve.service_time
                    else:
                        time += client_to_serve.service_time # if we arrive on time we just add the time
                        
                        # si no se debe esperar entonces se carga solamente el tiempo de servicio
                        self.tiempo_total_vehiculos += client_to_serve.service_time 

                # si no puede llegar o completar el servicio en la ventana de tiempo
                else:
                    new_genes_valid_time.append(0) # Add new truck
                    self.cantidad_vehiculos+=1 # se añade un vehículo a la cantidad
                    time = client_to_serve.ready_time + client_to_serve.service_time # Restart time because this is a new truck
                    position = client_to_serve
                    

                    # se suma la distancia del deposito al destino (por ser un nuevo vehículo) + tiempo de servicio
                    pos_depot = self.depot_data
                    self.tiempo_total_vehiculos += pos_depot.get_distance_to_client( client_to_serve ) + client_to_serve.service_time
                    # además también debemos sumar el tiempo que le tarda al vehículo viejo en volver al deposito
                    self.tiempo_total_vehiculos += position.get_distance_to_client( pos_depot )
                    # y restamos el tiempo del viejo al cliente ya que al final no fue
                    self.tiempo_total_vehiculos -= position.get_distance_to_client( client_to_serve )             
            new_genes_valid_time.append(client_number)
        
        self.genes = new_genes_valid_time

    def get_fitness(self):
    # retorna los dos valores de fitness del individuo: cantidad de vehiculos y la suma de los tiempos de cada vehículo
        return self.cantidad_vehiculos, self.tiempo_total_vehiculos

    def get_ruta(self):
    # retorna la ruta del individuo
        return self.genes

    def __init__(self, depot_data, clients_data, max_capacity):
        self.clients_data = clients_data
        self.depot_data = depot_data
        self.max_capacity = max_capacity
        # iniciamos esta variable en 1 porque en la función de fitness vamos sumando cada vez que aparece un nuevo vehículo
        # por lo que no se tiene en cuenta el primer vehículo
        self.cantidad_vehiculos = 1;
        self.tiempo_total_vehiculos = 0;
        self.generate_random_individual()
        self.heuristic_repair_and_fitness()