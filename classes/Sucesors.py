import math
import random

class NSGA(object):
    def __init__(self):
        self.population_size = 100
        self.elitism_prob = 0.1
        self.crossover_prob = 0.9
        self.mutation_prob = 0.05
        self.mutation_rate = 0.05
        self.population_list = [[3,5,6,7,1,4,9,8,2,10],[3,5,6,7,1,4,9,8,2,10],[3,5,6,7,1,4,9,8,2,10]]
        self.sucesors_list = []
    
    def elitist_selection(self, population):
        # cant is the amount of elements of the population to be select with elistism
        cant = self.population_size*self.elitism_prob
        # we select the 'cant' elements and append to the sucesors list
        for ind in range(0,cant):
            self.sucesors_list.append(self.population_list[ind])

    def crossover(self, indiv1, indiv2):
        size = min(len(indiv1), len(indiv2))
        # first we choose the two cutting points
        a, b = random.sample(range(size), 2)
        if a > b:
            a, b = b, a

    def mutation(self):
        # first we calculate the amount of elements to be mutated
        cant = math.ceil(self.mutation_prob * len(self.population_list))
        # then we choose those elements
        for i in range(0,cant):
            indiv = random.choice(self.population_list)
            # for each element we mutate every gene with a probability of 0.05
            size = len(indiv)
            for g in range(size):
                if( random.random() <= self.mutation_rate ):
                    # if there will be a mutation we choose another gen index and we swap both
                    swap = random.randint(0,size-1)
                    while swap == g:
                        swap = random.randint(0,size-1)
                    print(indiv[g],indiv[swap])
                    indiv[g],indiv[swap] = indiv[swap],indiv[i]
