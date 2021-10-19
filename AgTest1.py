import random
import copy

NUMBER_ORGANISMS = 100
NUMBER_GENES = 9
GOAL = [1,2,3,4,5,6,7,8,9]
MAXIMUN_FITNESS = 9 
MUTATION_RATE = 0.001

def initializeOrganisms():
    organisms = []
    for _ in range(NUMBER_ORGANISMS):
        randomArray = [random.randint(1,9) for _ in range(0,NUMBER_GENES)]
        organisms.append({
            "genes":randomArray,
            "fitness": 0
        })
    return organisms

def evaluateOrganisms(organisms):
    totalFitness = 0
    for orgIndex in range(NUMBER_ORGANISMS):
        currentOrganismsFitnessTally = 0
        for i in range(NUMBER_GENES):
            if( organisms[orgIndex]["genes"][i] == GOAL[i] ):
                currentOrganismsFitnessTally+=1
        organisms[orgIndex]["fitness"] = currentOrganismsFitnessTally
        totalFitness += currentOrganismsFitnessTally
        if(currentOrganismsFitnessTally == MAXIMUN_FITNESS):
            return True
    return False

def org_get_total_fitness(orgs):
    totalFitness = 0 
    for fitness in [ org["fitness"] for org in  orgs]:
        totalFitness += fitness
    return totalFitness

def get_best_from_orgs(orgs):
    best = orgs[0]
    for i in range(NUMBER_ORGANISMS):
        if( orgs[i]["fitness"] > best["fitness"] ):
            best = orgs[i]
    return best

def get_avg_from_orgs(orgs):
    return org_get_total_fitness(orgs) / NUMBER_ORGANISMS

def selectOneOrganism(organisms):
    totalFitness = org_get_total_fitness(organisms)
    randomSelectPoint = random.randint(1,totalFitness)
    runningTotal = 0
    for i in range(NUMBER_ORGANISMS):
        runningTotal += organisms[i]["fitness"]
        if runningTotal >= randomSelectPoint:
            return organisms[i]["genes"]
        

def produceNextGeneration(organisms):
    nextGeneration = copy.deepcopy(organisms)
    for orgIndex in range(NUMBER_ORGANISMS):
        dad = selectOneOrganism(organisms)
        mom = selectOneOrganism(organisms)
        crossOverPoint = random.randint(0, NUMBER_GENES)
        for j in range(NUMBER_GENES):
            mutateThisGene = random.randint( 1,int(1/MUTATION_RATE) )
            if(mutateThisGene == 1): #        // we decided to make this gene a mutation
                nextGeneration[orgIndex]["genes"][j] = random.randint(1,9)
            else:
                #// we decided to copy this gene from a parent
                if j < crossOverPoint:
                    nextGeneration[orgIndex]["genes"][j] = dad[j]
                else:
                    nextGeneration[orgIndex]["genes"][j] = mom[j]
    return nextGeneration
    

def doOneRun():
    generationCount = 0
    orgs = initializeOrganisms()
    while(True):
        perfectGeneration = evaluateOrganisms(orgs)
        best = get_best_from_orgs(orgs)
        print ("{:<8} {:<20} {:<15} {:<15}".format(generationCount, org_get_total_fitness(orgs), get_avg_from_orgs(orgs), best["fitness"] ), best["genes"] )
        if( perfectGeneration ):
            return generationCount
        orgs = produceNextGeneration(orgs)
        generationCount+=1

def main():
    print('AG testing 1')
    print('The goal is to generate this array:\n[1, 2, 3, 4, 5, 6, 7, 8, 9]')
    print ("{:<8} {:<20} {:<15} {:<15} {:<25}".format("Gen #", "Total Fitness", "Avg Fitness", "Best Fitness", "Best"))
    orgs = initializeOrganisms()
    evaluateOrganisms(orgs)
    finalGeneration = doOneRun()
    #print("The final generation was: ", finalGeneration)
main()