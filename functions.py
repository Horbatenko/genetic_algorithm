from random import randint, sample, choice
from math import sqrt
from settings import SCREEN_SIZE, START_POINT_POS, FONT_SIZE


def generate_cities(cities_num):
    return [
        {
            'id': i,
            'pos': (  # 'minus FONT_SIZE' - to print numbers not out of the screen
                randint(0, SCREEN_SIZE[0] - FONT_SIZE),
                randint(0, SCREEN_SIZE[1] - FONT_SIZE)
            )
        } for i in range(cities_num)
    ]


def generate_individuals(population_size, cities):
    cities_num = len(cities)
    return [
        {
            'genome': sample(cities, cities_num),
            'score': 0,
        } for i in range(population_size)
    ]


def calculate_score(points, distance=0, last_point=START_POINT_POS):
    current_point = points.pop(0)

    distance += get_distance_between_points(last_point, current_point)

    if not points:
        distance += get_distance_between_points(current_point, START_POINT_POS)  # start -> points -> start
        return distance

    return calculate_score(points, distance, last_point=current_point)


def get_distance_between_points(p1, p2):
    return sqrt(
        (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    )


def get_route_from_individual(individual):
    return [city['pos'] for city in individual['genome']]


def get_cities_ids_from_individual(individual):
    return [city['id'] for city in individual['genome']]


def create_child(parent1, parent2):
    # https://www.youtube.com/watch?v=DJ-yBmEEkgA
    def build_cycles(p1, p2, start_index):
        cycle1 = {}
        cycle2 = {}

        while start_index not in cycle1:
            cycle1[start_index] = p1[start_index]

            p2_val = p2[start_index]

            cycle2[start_index] = p2_val

            start_index = p1.index(p2_val)

        return cycle1, cycle2

    parent_genome_1 = parent1['genome']
    parent_genome_2 = parent2['genome']

    cycles_set1 = []
    cycles_set2 = []

    for index, val in enumerate(parent_genome_1):
        if any([index in cycle for cycle in cycles_set1]):  # element already in cycles
            continue

        cycle1, cycle2 = build_cycles(parent_genome_1, parent_genome_2, index)

        cycles_set1.append(cycle1)
        cycles_set2.append(cycle2)

    child = {
        'score': 0,
        'genome': [None] * len(parent_genome_1)
    }

    for c1, c2 in zip(cycles_set1, cycles_set2):
        c = choice([c1, c2])
        for key in c:
            child['genome'][key] = c[key]

    return child
