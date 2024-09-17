from neural_net import NeuralNet
import numpy as np
import random
import time
from client import Client

"""
The genetic algorithm using the simple fitness function of just distance raced
"""

def run_GA():
    """
    Runs genetic algorithm training sessions
    """

    for i in range(5):
        best_fitnesses = []
        average_fitnesses = []
        population = initialise_pop(8, 4)

        for g in range(120):
            # produce children from crossing over pairs of chromosomes
            children = crossover(population)

            # mutate each child slightly
            mutated_children = mutation(children)

            # test the children
            evaluated_children, max_time_count = run_children(mutated_children)

            # combine the populations
            extended_population = population + evaluated_children

            # select the best half of the population to remain
            population, worst, average = selection(extended_population)

            display_gen(g, worst, average, population[0][0], population[len(population)-1][0], max_time_count)

            # save the metrics for the generation
            best_fitnesses.append(population[0][0])
            average_fitnesses.append(average)
            save_gen(population, best_fitnesses, average_fitnesses, i)

def mutation(children):
    mutated_children = []
    for c in children: # for each child, add random noise to the chromosome
        child_chromosome = c + np.random.normal(loc=0,scale=0.1,size=(NeuralNet.chromosome_length))
        mutated_children.append(child_chromosome)
    
    return mutated_children

def crossover(population):
    """
    Creates children from the population using single point crossover
    """

    children = []

    indices = list(range(len(population)))
    for i in range(len(population)//2):
        # decide which parents should breed
        index1, index2 = random.sample(indices, 2)
        indices.remove(index1)
        indices.remove(index2)

        # retrieve the parent chromosomes
        parent1 = population[index1][1]
        parent2 = population[index2][1]

        # determine the crossover point and generate children
        crossover_point = np.random.randint(1, NeuralNet.chromosome_length - 1)
        child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))

        children.append(child1)
        children.append(child2)

    return children

def run_bot(agent):
    """
    Run a single agent in the game
    """

    max_time = 0

    # run the race for a number of steps
    for step in range(C.maxSteps, 0, -1):
        C.get_servers_input()
        r = agent.drive(C.S, C.R)
        C.update(r)
        C.respond_to_server()

        # early stopping for crashed or off track cars
        if (C.S.d['speedX'] < 20 or C.S.d['trackPos'] > 1 or C.S.d['trackPos'] < -1) and step < (C.maxSteps - 400):
            break
        
        if step == 1: # tracks which agents hit the time limit
            max_time = 1
    
    return max_time

def display_gen(generation, worst_fitness, average_fitness, best_fitness, last_kept_fitness, max_time_count):
    print()
    print("-----------------------------------------------------------------------")
    print()
    
    print("Generation " + str(generation) + " Complete")
    print("Training time so far: {:.2f}".format((time.time() - START_TIME) / 60) + " mins")
    print()

    print("     Best Fitness: {:.3f}".format(best_fitness))
    print("     Last Kept Fitness: {:.3f}".format(last_kept_fitness))
    print("     Worst Fitness: {:.3f}".format(worst_fitness))
    print("     Average Fitness: {:.3f}".format(average_fitness))
    print("     Bots that ran out of time: " + str(max_time_count))

    print()
    print("-----------------------------------------------------------------------")
    print()

def save_gen(population, best, average, i):
    """
    Save the state of training to avoid crash issues and metrics for graphs
    """
    chromosomes = []
    for p in population:
        chromosomes.append(p[1])
    np.savetxt("GA/Fitness/chromosomes" + str(i) + ".txt", np.array(chromosomes))
    np.savetxt("GA/Fitness/best" + str(i) + ".txt", np.array(best))
    np.savetxt("GA/Fitness/average" + str(i) + ".txt", np.array(average))

def selection(population):
    """
    Selects the best half of the population to progress to the next generation, discarding the rest
    """

    population.sort(key=lambda x: x[0], reverse=True)
    total = 0
    for p in population:
        total += p[0]
    return population[:len(population)//2], population[len(population)-1][0], total/len(population)

def run_children(children):
    """
    Runs each child in the game separately to obtain its fitness
    """

    child_population = []
    max_time_count = 0

    for chromosome in children:
        agent = NeuralNet(chromosome) # create agent from chromosome
        max_time_count += run_bot(agent)
        fitness = fitness_function()
        child_population.append((fitness, chromosome))

        # reset race
        C.R.d['meta'] = 1
    
    return child_population, max_time_count

def initialise_pop(random, zeroes):
    """
    Initialise the population of random chromosomes
    The zeroes argument allows for the creation of chromosomes that are filled with 0's
    """

    population = []
    for i in range(random):
        chromosome = np.random.uniform(-1, 1, NeuralNet.chromosome_length)
        agent = NeuralNet(chromosome)
        run_bot(agent) # test the agent for its fitness
        fitness = fitness_function()
        population.append((fitness, chromosome))

        # reset race
        C.R.d['meta'] = 1

    for i in range(zeroes):
        chromosome = np.zeros(NeuralNet.chromosome_length)
        agent = NeuralNet(chromosome)
        run_bot(agent) # test the agent for its fitness
        fitness = fitness_function()
        population.append((fitness, chromosome))

        # reset race
        C.R.d['meta'] = 1

    return population

def fitness_function():
    return C.S.d['distRaced']

# ================ MAIN ================
if __name__ == "__main__":
    START_TIME = time.time()
    C = Client()
    run_GA()
    C.shutdown()