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
        #borrar
        #[13, 91, 47, 0, 84, 0, 24, 35, 6, 0, 15, 0, 7, 22, 0, 95, 60, 75, 0, 100, 0, 11, 0, 17, 97, 0, 28, 0, 38, 0, 56, 0, 94, 74, 99, 0, 42, 41, 83, 1, 0, 61, 0, 5, 88, 0, 58, 64, 0, 71, 52, 0, 76, 45, 0, 81, 19, 0, 55, 40, 0, 10, 0, 67, 79, 0, 14, 12, 0, 9, 0, 16, 51, 0, 32, 85, 0, 30, 0, 96, 92, 48, 23, 21, 0, 59, 0, 82, 34, 66, 0, 
#       44, 0, 3, 36, 0, 87, 80, 0, 98, 69, 0, 70, 68, 49, 0, 86, 0, 90, 62, 8, 0, 63, 0, 26, 0, 25, 39, 0, 93, 0, 20, 2, 0, 65, 0, 57, 18, 46, 0, 27, 0, 54, 53, 77, 0, 72, 
#       0, 43, 0, 33, 37, 50, 0, 78, 31, 4, 0, 29, 89, 0, 73]
        # self.gen2 = [13, 91, 47, 84, 24, 35, 6, 15, 7, 22, 0, 95, 60, 75, 100, 11, 17, 97, 28, 0, 38, 56, 94, 74, 99, 42, 41, 83, 1, 61, 0, 5, 88, 58, 64, 71, 52, 76, 45, 81, 19, 55, 40, 0, 10, 67, 79, 14, 12, 9, 16, 51, 32, 85, 30, 0, 96, 92, 48, 23, 21, 59, 82, 34, 66, 44, 3, 36, 87, 80, 0, 98, 69, 70, 68, 49, 86, 90, 62, 8, 63, 0, 26, 25, 39, 93, 20, 2, 65, 0, 57, 18, 46, 27, 54, 53, 77, 72, 43, 0, 33, 37, 50, 78, 31, 4, 29, 89, 73]
        # new_genes_valid_capacity = [13, 91, 47, 84, 24, 35, 6, 15, 7, 22, 0, 95, 60, 75, 100, 11, 17, 97, 28, 0, 38, 56, 94, 74, 99, 42, 41, 83, 1, 61, 0, 5, 88, 58, 64, 71, 52, 76, 45, 81, 19, 55, 40, 0, 10, 67, 79, 14, 12, 9, 16, 51, 32, 85, 30, 0, 96, 92, 48, 23, 21, 59, 82, 34, 66, 44, 3, 36, 87, 80, 0, 98, 69, 70, 68, 49, 86, 90, 62, 8, 63, 0, 26, 25, 39, 93, 20, 2, 65, 0, 57, 18, 46, 27, 54, 53, 77, 72, 43, 0, 33, 37, 50, 78, 31, 4, 29, 89, 73]
        # self.gen2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
        # new_genes_valid_capacity = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
        
        #borrar
#       [13, 91, 47, 84, 24, 35, 6, 15, 7, 22, 0, 95, 60, 75, 100, 11, 17, 97, 28, 0, 38, 56, 94, 74, 99, 42, 41, 83, 1, 61, 0, 5, 88, 58, 64, 71, 52, 76, 45, 81, 19, 55, 40, 0, 10, 67, 79, 14, 12, 9, 16, 51, 32, 85, 30, 0, 96, 92, 48, 23, 21, 59, 82, 34, 66, 44, 3, 36, 87, 80, 0, 98, 69, 70, 68, 49, 86, 90, 62, 8, 63, 0, 26, 25, 39, 93, 20, 2, 65, 0, 57, 18, 46, 27, 54, 53, 77, 72, 43, 0, 33, 37, 50, 78, 31, 4, 29, 89, 73]
#       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
        
        new_genes_valid_time = []
        time = 0
        position = self.depot_data
        for client_number in new_genes_valid_capacity:
            if client_number == 0:
                time = 0# Restart time because this is a new truck
                position = self.depot_data
                #borrar
                # print('client number es 0, {}'.format(position.client_number))
            else:
                #borrar
                # print('no es cero, {} y {}'.format(position.client_number, client_number))
                client_to_serve = self.clients_data[ client_number - 1 ]
                #borrar
                # print("quiere ir a {}".format(client_to_serve.client_number))

                time +=  position.get_distance_to_client( client_to_serve )
                
                # Sumamos primero al tiempo total el tiempo en llegar del punto actual al destino
                self.tiempo_total_vehiculos += position.get_distance_to_client( client_to_serve ) 

                if client_to_serve.can_serve_in_timepoint(time):
                    # borrar
                    # print('no añadimos un 0 acá')
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
                    # borrar
                    # print('añadimos un 0 aca')
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
            
            # borrar
            # print('añadimos un {} aca'.format(client_number))
            new_genes_valid_time.append(client_number)
        
        self.genes = new_genes_valid_time

    def get_fitness(self):
    # retorna los dos valores de fitness del individuo: cantidad de vehiculos y la suma de los tiempos de cada vehículo
        return self.cantidad_vehiculos, self.tiempo_total_vehiculos

    def get_ruta(self):
    # retorna la ruta del individuo
        return self.genes

    #borrar
    # def get_gen2(self):
    #     return self.gen2

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