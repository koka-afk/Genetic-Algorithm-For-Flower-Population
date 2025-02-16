from Flower import flower
import random

mutation_rate = 0.05
population_size = 8

def init_population():
    global population
    population = [flower() for _ in range(population_size)]
    return population

def selection():
    population.sort(key=lambda x: x.fitness, reverse=True)
    # for x in population:
    #     print(f'pn: {x.petals_number}  fitness: {x.fitness}')


def crossover_numbers(number1, number2):
    b1 = list(bin(number1))
    b2 = list(bin(number2))
    if(len(b1) < len(b2)):
        dif = len(b2) - len(b1)
        b1[1] = '0'
        for i in range(dif):
            b1.insert(0, '0')
        b1[1] = 'b'
    else:
        dif = len(b1) - len(b2)
        b2[1] = '0'
        for i in range(dif):
            b2.insert(0, '0')
        b2[1] = 'b'
    
    b1 = "".join(b1)
    b2 = "".join(b2)

    pos = random.randint(2, len(b1) - 1)

    new1 = ""
    new2 = ""
    for i in range(pos):
        new1 += b1[i]
        new2 += b2[i]
    for i in range(pos, len(b1)):
        new1 += b2[i]
        new2 += b1[i]

    number1 = int(new1, 2)
    number2 = int(new2, 2)
    #print(f'pos: {pos} \n b1: {b1} \n b2: {b2} \n new1: {new1} \n new2: {new2} \n number1: {number1} \n number2: {number2}')

    return number1, number2

def crossover(parent1, parent2):
    child1 = flower()
    child2 = flower()
    center_size1, center_size2 = crossover_numbers(parent1.center_size, parent2.center_size)

    cr1, cr2 = crossover_numbers(parent1.center_color[0], parent2.center_color[0]) # center red
    cg1, cg2 = crossover_numbers(parent1.center_color[1], parent2.center_color[1]) # center green
    cb1, cb2 = crossover_numbers(parent1.center_color[2], parent2.center_color[2]) # center blue

    petals1, petals2 = crossover_numbers(parent1.petals_number, parent2.petals_number)

    pr1, pr2 = crossover_numbers(parent1.petals_color[0], parent2.petals_color[0]) # petals red
    pg1, pg2 = crossover_numbers(parent1.petals_color[1], parent2.petals_color[1]) # petals green
    pb1, pb2 = crossover_numbers(parent1.petals_color[2], parent2.petals_color[2]) # petals blue
    
    child1.center_size = center_size1
    child1.center_color = (cr1, cg1, cb1)
    child1.petals_number = petals1
    child1.petals_color = (pr1, pg1, pb1)

    child2.center_size = center_size2
    child2.center_color = (cr2, cg2, cb2)
    child2.petals_number = petals2
    child2.petals_color = (pr2, pg2, pb2)

    #fitness_factor = {7: 5000, 6: 2000, 5: 1000, 4: 500, 3: 250, 2: 100, 1: 50, 0:0}
    # child.center_size = random.choice([parent1.center_size, parent2.center_size])
    # child.center_color = tuple(random.choice([parent1.center_color[i], parent2.center_color[i]]) for i in range(3))
    # child.petals_number = random.choice([parent1.petals_number, parent2.petals_number])
    # child.petals_color = tuple(random.choice([parent1.petals_color[i], parent2.petals_color[i]]) for i in range(3))
    #child.fitness = (parent1.fitness + parent2.fitness) // 2 + fitness_factor[child.petals_number]
    return child1, child2

def mutate_color(number):
    shift_amount = random.randint(0, 6)
    number = (1 << shift_amount) ^ number
    return number

def mutate_petals(number):
    shift_amount = random.randint(0, 2)
    number = (1 << shift_amount) ^ number
    return number

def mutate(flower):
    if random.random() < mutation_rate:
        flower.center_size = random.randint(1, 20)
    if random.random() < mutation_rate:
        flower.center_color = (mutate_color(flower.center_color[0]), mutate_color(flower.center_color[1]), mutate_color(flower.center_color[2]))
    if random.random() < mutation_rate:
        flower.petals_number = mutate_petals(flower.petals_number)
    if random.random() < mutation_rate:
        flower.petals_color = (mutate_color(flower.petals_color[0]), mutate_color(flower.petals_color[1]), mutate_color(flower.petals_color[2]))

def evolve_population():    
    selection()
    new_population = []
    idx = 0
    for i in range(2):
        parent1 = population[idx]
        parent2 = population[idx + 1]
        child1, child2 = crossover(parent1, parent2)
        mutate(child1)
        mutate(child2)
        new_population.extend([parent1, parent2, child1, child2])
        idx += 2

    # Replace old population with the new generation
    population[:] = new_population
        
