from app import App


def main():
    app = App(
        cities_num=10,  # this >= 2
        population_size=30,  # this > 2
        next_round_passers_num=10,  # 2 <= this < population_size
        mutation_chance=1  # 0 <= this <= 1
    )
    app.run()


if __name__ == '__main__':
    main()
