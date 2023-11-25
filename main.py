import random

backpack_capacity = 6404180

will_mutate = 0.5

items = [
    [1, 'Toporek', 32252, 68674],
    [2, 'Moneta z brązu', 225790, 471010],
    [3, 'Korona', 468164, 944620],
    [4, 'Diamentowy posążek', 489494, 962094],
    [5, 'Szmaragdowy pas', 35384, 78344],
    [6, 'Skamieliny', 265590, 579152],
    [7, 'Złota moneta', 497911, 902698],
    [8, 'Hełm', 800493, 1686515],
    [9, 'Tusz', 823576, 1688691],
    [10, 'Szkatułka', 552202, 1056157],
    [11, 'Nóż', 323618, 677562],
    [12, 'Długi miecz', 382846, 833132],
    [13, 'Maska', 44676, 99192],
    [14, 'Naszyjnik', 169738, 376418],
    [15, 'Opalowa zawieszka', 610876, 1253986],
    [16, 'Perły', 854190, 1853562],
    [17, 'Kołczan', 671123, 1320297],
    [18, 'Rubinowy pierścień', 698180, 1301637],
    [19, 'Srebrna bransoletka', 446517, 859835],
    [20, 'Czasomierz', 909620, 1677534],
    [21, 'Mundur', 904818, 1910501],
    [22, 'Trucizna', 730061, 1528646],
    [23, 'Wełniany szal', 931932, 1827477],
    [24, 'Kusza', 952360, 2068204],
    [25, 'Stara księga', 926023, 1746556],
    [26, 'Puchar z cynku', 978724, 2100851]
]


def create_population(population_size, individual_size):
    population = []
    for individual in range(0, population_size):
        individual = []
        for gene in range(0, individual_size):
            gene = random.randint(0,1)
            individual.append(gene)
        population.append(individual)
    return population


def measuring_adaptation(individual: []):
    weight = 0
    value = 0
    for gene in individual:
        bit = individual[gene]
        if bit == 1:
            weight = weight + items[gene][2]
            value = value + items[gene][3]
    if weight > backpack_capacity:
        return 0
    return weight, value


def adaptation_in_population(population):
    overall = 0
    output = 0
    for individual in population:
        overall, _ = overall + measuring_adaptation(individual)
    for individual in population:
        individual.append(output, _ = measuring_adaptation(individual) / overall)


def roulette(population, chosen_amount):
    adaptation_in_population(pop)
    compartments = []
    sum = 0
    for i in range(chosen_amount):
        compartments.append([i, sum, sum + population[i][len(population[0])]])
        sum = sum + population[i][len(population[0])]
    rand = random.uniform(0, 1)
    result = [compartment for compartment in compartments if compartment[1] < rand <= compartment[2]]
    return result


def crossing_single_point(parent_a, parent_b, point):
    children = []
    kid_1 = parent_a[:point] + parent_b[point:]
    children.append(kid_1)

    kid_2 = parent_b[:point] + parent_a[point:]
    children.append(kid_2)
    return children


def mutation(individual, length):
    index = random.randint(0, length)
    if individual[index] == 1:
        individual[index] = 0
    else:
        individual[index] = 1


# def best_in_population(population):



if __name__ == '__main__':
    pop = create_population(10, 26)
    adaptation_in_population(pop)
    parents = roulette(pop, 5)
    children = []
    for i in parents:
        for j in parents:
            if i != j:
                children.append(crossing_single_point(i, j, 12))
    for kid in children:
        if random.uniform(0, 1) > will_mutate:
            mutation(kid, 25)
    new_pop = roulette(children, 10)
    adaptation_in_population(new_pop)




