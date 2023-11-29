import random
import matplotlib.pyplot as plt
from time import perf_counter

backpack_capacity = 6404180

will_mutate = 0.01

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


class Individual:
    def __init__(self, genes):
        self.genes = genes
        self.adaptation = self.calculate_adaptation()
        self.value = self.calculate_value()

    def calculate_adaptation(self):
        weight = 0
        for gene, bit in enumerate(self.genes):
            if bit == 1:
                weight += items[gene][2]
        return weight if weight <= backpack_capacity else 0

    def calculate_value(self):
        value = 0
        for gene, bit in enumerate(self.genes):
            if bit == 1:
                value += items[gene][3]
        return value

    def mutate(self):
        index = random.randint(0, len(self.genes) - 1)
        if random.random() < will_mutate:
            self.genes[index] = 1 - self.genes[index]
            self.adaptation = self.calculate_adaptation()
            self.value = self.calculate_value()

    def __repr__(self):
        return f"Genes: {self.genes}, Adaptation: {self.adaptation}, Value: {self.value}"


def create_population(population_size, individual_size):
    population = []
    for _ in range(population_size):
        genes = [random.randint(0, 1) for _ in range(individual_size)]
        individual = Individual(genes)
        population.append(individual)
    return population


def roulette(population, chosen_amount):
    total_fitness = sum(individual.adaptation for individual in population)
    compartments = []
    sum_prob = 0

    for i, individual in enumerate(population):
        probability = individual.adaptation / total_fitness
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


def tournament_selection(population, parents_amount):
    tmp_population = population.copy()
    random.shuffle(tmp_population)
    groups = []

    increment = int(len(population)/parents_amount)
    groups.append(tmp_population[:increment])

    for i in range(1, parents_amount + 1):
        if i == parents_amount + 1:
            groups.append(tmp_population[i * increment:-1])
        else:
            groups.append(tmp_population[i*increment:(i+1)*increment])

    parents = []

    for group in groups:
        kid = max(group, key=lambda x: x.adaptation)
        parents.append(kid)

    return parents


def crossing_double_point(parent_a, parent_b, point1, point2=18):
    genes_a = parent_a.genes
    genes_b = parent_b.genes
    children = []
    kid_1 = Individual(genes_a[:point1] + genes_b[point1:point2] + genes_a[point2:])
    children.append(kid_1)
    kid_2 = Individual(genes_b[:point1] + genes_a[point1:point2] + genes_b[point2:])
    children.append(kid_2)
    return children


def crossing_single_point(parent_a, parent_b, point):
    genes_a = parent_a.genes
    genes_b = parent_b.genes
    children = []
    kid_1 = Individual(genes_a[:point] + genes_b[point:])
    children.append(kid_1)
    kid_2 = Individual(genes_b[:point] + genes_a[point:])
    children.append(kid_2)
    return children


def best_in_population(population):
    max_element = max(population, key=lambda x: x.adaptation)
    return max_element


def cut_from_population(population_size, population):
    new_population = roulette(population, population_size)
    return new_population


def ag(population_size, generations_amount, parents_amount, selection_func, crossing_func):
    global_pop = create_population(population_size, 26)
    best_kid = None
    best_kids = []
    for generation in range(generations_amount):
        best_in_pop = best_in_population(global_pop)
        best_kids.append(best_in_pop)
        if not best_kid or best_in_pop.adaptation > best_kid.adaptation:
            best_kid = best_in_pop
        parents = selection_func(global_pop, parents_amount)
        children = []
        for parent_a in parents:
            for parent_b in parents:
                if parent_a != parent_b:
                    resulting_children = crossing_func(parent_a, parent_b, 8)
                    children.extend(resulting_children)
        for kid in children:
            kid.mutate()
        global_pop.extend(children)
        global_pop = cut_from_population(population_size, global_pop)

    return best_kid, best_kids


if __name__ == '__main__':
    ag1_start = perf_counter()
    result, best_kids1 = ag(10000, 90, 110, roulette, crossing_single_point)
    ag1_stop = perf_counter()
    ag2_start = perf_counter()
    result2, best_kids2 = ag(10000, 90, 110, tournament_selection, crossing_double_point)
    ag2_stop = perf_counter()
    print("____________Wynik dla selekcji ruletki oraz krzyżowania jednopunktowego____________")
    print("Najlepsze dziecko: ", result)
    print("Wartość przedmiotów: ", result.value)
    print("Czas wykonywania: ", ag1_stop - ag1_start)

    print("____________Wynik dla selekcji turniejowej oraz krzyżowania dwupunktowego____________")
    print("Najlepsze dziecko: ", result2)
    print("Wartość przedmiotów: ", result2.value)
    print("Czas wykonywania: ", ag2_stop - ag2_start)

    fig, ax = plt.subplots(1, 2, constrained_layout=True)
    fig.set_size_inches(8, 4)
    fig.suptitle('Parametry:\npopulacja: 10000 | liczba generacji: 90 | liczba rodziców: 110')
    x1 = [x.adaptation for x in best_kids1]
    x2 = [x.adaptation for x in best_kids2]
    ax[0].plot(list(range(len(x1))), x1)
    ax[0].set_title("selekcja ruletki\nkrzyżowanie jednopunktowe")
    ax[0].grid(True)
    ax[1].plot(list(range(len(x2))), x2)
    ax[1].set_title("selekcja turniejowa\nkrzyżowanie dwupunktowe")
    ax[1].grid(True)
    plt.show()

    ag1_start = perf_counter()
    result, best_kids1 = ag(10000, 90, 110, roulette, crossing_double_point)
    ag1_stop = perf_counter()
    ag2_start = perf_counter()
    result2, best_kids2 = ag(10000, 90, 110, tournament_selection, crossing_single_point)
    ag2_stop = perf_counter()
    print("____________Wynik dla selekcji ruletki oraz krzyżowania dwupunktowego____________")
    print("Najlepsze dziecko: ", result)
    print("Wartość przedmiotów: ", result.value)
    print("Czas wykonywania: ", ag1_stop - ag1_start)

    print("____________Wynik dla selekcji turniejowej oraz krzyżowania jednopunktowego____________")
    print("Najlepsze dziecko: ", result2)
    print("Wartość przedmiotów: ", result2.value)
    print("Czas wykonywania: ", ag2_stop - ag2_start)

    fig, ax = plt.subplots(1, 2, constrained_layout=True)
    fig.set_size_inches(8, 4)
    fig.suptitle('Parametry:\npopulacja: 10000 | liczba generacji: 90 | liczba rodziców: 110')
    x1 = [x.adaptation for x in best_kids1]
    x2 = [x.adaptation for x in best_kids2]
    ax[0].plot(list(range(len(x1))), x1)
    ax[0].set_title("selekcja ruletki\nkrzyżowanie dwupunktowe")
    ax[0].grid(True)
    ax[1].plot(list(range(len(x2))), x2)
    ax[1].set_title("selekcja turniejowa\nkrzyżowanie jednopunktowe")
    ax[1].grid(True)
    plt.show()
