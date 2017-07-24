import random
import sys

DNASize = 11
MutationChance = 9
CrossoverChance = 8

class DNA:
    def __init__(self):
        self.DNA = self.generateDNA()

    def generateGene(self):
        gene = random.randint(0, 1)
        return gene 

    def generateDNA(self):
        DNA = ''

        for i in range(0, DNASize):
            gene = self.generateGene()
            DNA = DNA + str(gene)

        return DNA

    def getGene(self, index): return self.DNA[index]

    def changeDNA(self, index, gene):
        self.DNA = self.DNA[0:index] + str(gene) + self.DNA[index+1:]

    def mutate(self):
        for i in range(0, DNASize):
            if random.randint(0, 10) >= MutationChance:
                gene = self.generateGene()
                self.changeDNA(i, gene)


def crossover(first, second):
    newDNA = DNA()

    for i in range(0, DNASize): 
        if first.DNA[i] == second.DNA[i]:
            if random.randint(0, 10) >= CrossoverChance:
                newDNA.changeDNA(i, first.DNA[i])

    return newDNA

class Machine:
    def __init__(self, initialValue, DNA):    
        self.DNA = DNA
        self.initialValue = initialValue
        self.value = 0


    def process(self):
        self.value = 0

        for i in range(0, DNASize):
            if self.DNA.getGene(i) == '0':
                self.value = self.value - self.initialValue
            else:
                self.value = self.value + self.initialValue

        return self.value

def machineFitness(output, target):
    return abs(target - output)

if __name__ == '__main__':

    target = int(sys.argv[1])

    initialCreatures = int(sys.argv[2])
    childrenCreatures = int(sys.argv[3])
    topCreatures = int(sys.argv[4])

    DNAs = []

    for i in range(0, initialCreatures):
        DNAs.append(DNA())

    Machines = []

    for i in range(0, initialCreatures):
        value = random.randint(0, 100)
        Machines.append(Machine(value, DNAs[i]))

    fitnesses = initialCreatures * [ -1 ]

    it = 1

    while 0 not in fitnesses:
        print("Iteration #{0}".format(it))

        for i in range(0, len(Machines)):
            value = Machines[i].process()
            fitness = machineFitness(value, target)

            fitnesses[i] = fitness

        sorted(Machines, key=lambda machine: machineFitness(machine.value, target))
        fitnesses.sort()
        topMachines = Machines[:topCreatures]

        for i in range(0, childrenCreatures):
            parents = random.sample(set(range(0, topCreatures - 1)), 2)

            newDNA = crossover(topMachines[parents[0]].DNA, topMachines[parents[1]].DNA)
            newDNA.mutate()

            Machines[i] = Machine(random.randint(0, 100), newDNA)

        Machines = Machines[:childrenCreatures]
        fitnesses = fitnesses[:childrenCreatures]

#        if fitnesses == lastFitnesses:
#            break

        print(fitnesses)

        it = it + 1

    print(fitnesses[:topCreatures])


