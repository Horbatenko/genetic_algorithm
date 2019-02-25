import pygame
import random
from sty import fg
from functions import (
    generate_cities, generate_individuals,
    get_route_from_individual, get_cities_ids_from_individual,
    create_child, calculate_score
)
from settings import (
    SCREEN_SIZE, BACKGROUND_COLOR,
    FONT_STYLE, FONT_SIZE, FONT_COLOR,
    START_POINT_POS, START_POINT_COLOR, START_POINT_RADIUS
)


pygame.font.init()


class App:
    def __init__(self, cities_num, population_size, next_round_passers_num, mutation_chance):
        if not cities_num >= 2:
            raise ValueError('Wrong value for cities_num (cities_num >= 2)')
        if not population_size > 2:
            raise ValueError('Wrong value for population_size (population_size > 2)')
        if not 0 < next_round_passers_num < population_size:
            raise ValueError('Wrong value for next_round_passers_num (0 < val < population_size)')
        if not 0 <= mutation_chance <= 1:
            raise ValueError('Wrong value for mutation_chance (0 < val < 1)')

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen.fill(BACKGROUND_COLOR)
        self.font = pygame.font.SysFont(FONT_STYLE, FONT_SIZE)
        pygame.display.set_caption('Genetic algo')

        self.cities = generate_cities(cities_num)
        self.generation = Generation(population_size, next_round_passers_num, mutation_chance, self.cities)
        self.routes_to_be_displayed = []

    def run(self):

        running = True

        while running:
            generation_winner = self.generation.get_generation_winners()[0]
            self.add_route(  # display the best route from generation
                get_route_from_individual(generation_winner),
                {
                    'route': get_cities_ids_from_individual(generation_winner),
                    'score': generation_winner['score']
                }
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.refresh_screen()

            self.generation.make_new_generation()

    def draw_cities(self):
        for city in self.cities:
            text_surface = self.font.render(
                str(city['id']), False, FONT_COLOR
            )
            self.screen.blit(text_surface, city['pos'])

    def draw_start_point(self):
        pygame.draw.circle(
            self.screen, START_POINT_COLOR, START_POINT_POS, START_POINT_RADIUS
        )

    def draw_routes(self):
        for route_obj in self.routes_to_be_displayed:
            pygame.draw.lines(
                self.screen, route_obj['color'], True,
                [START_POINT_POS] + route_obj['route'], 2
            )

    def add_route(self, route, log_info=None):
        # if there is no route like the given one
        if route not in [route_obj['route'] for route_obj in self.routes_to_be_displayed]:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            route_obj = {
                'route': route,
                'color': color,
            }
            self.routes_to_be_displayed.append(route_obj)
            if log_info:
                log = fg(*color) + str(log_info) + fg.rs
                print(log)

    def refresh_screen(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_start_point()
        self.draw_routes()
        self.draw_cities()

        pygame.display.flip()


class Generation:
    def __init__(self, population_size, next_round_passers_num, mutation_chance, cities):
        self.generation_number = 0
        self.mutation_chance = mutation_chance
        self.population_size = population_size
        self.individuals = generate_individuals(self.population_size, cities)
        self.next_round_passers_num = next_round_passers_num

    def calc_individuals_score(self):
        for individual in self.individuals:
            individual['score'] = calculate_score(
                get_route_from_individual(individual)
            )

    def get_generation_winners(self):
        self.calc_individuals_score()

        self.individuals = sorted(
            self.individuals, key=lambda i: i['score']
        )[:self.next_round_passers_num]

        return self.individuals

    def make_new_generation(self):
        if random.uniform(0, 1) <= self.mutation_chance:
            self.mutate()

        current_population_size = len(self.individuals)
        parents = self.individuals[:]

        while current_population_size != self.population_size:
            parent1, parent2 = random.choices(parents, k=2)
            self.individuals.append(
                create_child(parent1, parent2)
            )

            current_population_size += 1

        self.generation_number += 1

    def mutate(self):
        individual = random.choice(self.individuals)
        genome = individual['genome']
        gene1, gene2 = random.choices(genome, k=2)
        i1 = genome.index(gene1)
        i2 = genome.index(gene2)
        genome[i1], genome[i2] = genome[i2], genome[i1]

    def log_individuals_info(self):
        for individual in self.individuals:
            print(individual['genome'], individual['score'])
        print('------------------------')
