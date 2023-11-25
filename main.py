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
    for gene in range(len(individual)):
        bit = individual[gene]
        if bit == 1:
            weight = weight + items[gene][2]
    if weight > backpack_capacity:
        return 0
    return weight


def measuring_value(individual: []):
    value = 0
    for gene in range(len(individual)):
        bit = individual[gene]
        if bit == 1:
            value = value + items[gene][3]
    return value


def adaptation_in_population(population):
    overall = 0
    for individual in population:
        overall = overall + measuring_adaptation(individual)
    for individual in population:
        individual.append(measuring_adaptation(individual) / overall)
    return overall


def roulette(population, chosen_amount):
    compartments = []
    total_fitness = sum(individual[-1] for individual in population)
    sum_prob = 0

    for i, individual in enumerate(population):
        probability = individual[-1] / total_fitness
        compartments.append([i, sum_prob, sum_prob + probability])
        sum_prob += probability

    selected = []
    for _ in range(chosen_amount):
        rand = random.uniform(0, 1)
        for compartment in compartments:
            if compartment[1] < rand <= compartment[2]:
                selected.append(population[compartment[0]])
                break

    return selected


def crossing_single_point(parent_a, parent_b, point):
    children = []
    kid_1 = parent_a[:point] + parent_b[point:]
    children.append(kid_1)

    kid_2 = parent_b[:point] + parent_a[point:]
    children.append(kid_2)
    return children


def mutation(individual):
    index = random.randint(0, len(individual)-1)
    if individual[index] == 1:
        individual[index] = 0
    else:
        individual[index] = 1

def best_in_population(population):
    max_element = max(population, key=lambda x: x[-1])
    return max_element


if __name__ == '__main__':
    pop = create_population(10, 26)
    print("Populacja pierwsza: ", len(pop))
    adaptation_in_population(pop)
    parents = roulette(pop, 5)
    print("Rodzice: ", len(parents))
    for kid in parents:
        kid.pop()
    children = []
    for parent_a in parents:
        for parent_b in parents:
            if parent_a != parent_b:
                resulting_children = crossing_single_point(parent_a, parent_b, 12)
                children.extend(resulting_children)
    print("Dzieci: ", len(children))
    for kid in children:
        mutation(kid)
    adaptation_in_population(children)
    new_pop = roulette(children, 10)
    print("Nowa populacja: ", len(new_pop))
    kid = best_in_population(new_pop)
    value = measuring_value(kid)
    print(kid)
    print(value)









