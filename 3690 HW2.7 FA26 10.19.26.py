
import random


def fitness(chromosome, power=2):
    x = int("".join(map(str, chromosome)), 2)
    return x ** power

def createPopulation(populationSize, chromosomeLength, rng):
    return [
        [rng.randint(0, 1) for _ in range(chromosomeLength)]
        for _ in range(populationSize)
    ]

def selection(population, fitnessFunction, rng):
    competitors = rng.sample(population, 2)
    return max(competitors, key=fitnessFunction).copy()


def crossover(parent1, parent2, rng):
    point = rng.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]


def mutate(chromosome, mutationRate, rng):
    for i in range(len(chromosome)):
        if rng.random() < mutationRate:
            chromosome[i] = 1 - chromosome[i]

    return chromosome

def geneticAlgorithm(
    populationSize=10,
    chromosomeLength=5,
    generations=20,
    mutationRate=0.1,
    power=2,
    seed=None
):
    if populationSize < 2:
        raise ValueError("Population size must be at least 2.")

    if chromosomeLength < 2:
        raise ValueError("Chromosome length must be at least 2.")

    if generations < 1:
        raise ValueError("Generations must be at least 1.")

    if not 0 <= mutationRate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1.")

    if not isinstance(power, int) or power < 1:
        raise ValueError("Power must be a positive integer.")

    rng = random.Random(seed)

    fitnessFunction = lambda chromosome: fitness(chromosome, power)

    population = createPopulation(
        populationSize, chromosomeLength, rng
    )

    maxX = 2 ** chromosomeLength - 1
    optimalFitness = maxX ** power

    best = None
    generationReached = 0

    for generation in range(1, generations + 1):
        best = max(population, key=fitnessFunction)
        generationReached = generation

        print(
            f"Generation {generation}: "
            f"Best = {best}, "
            f"Fitness = {fitnessFunction(best)}"
        )

        if fitnessFunction(best) == optimalFitness:
            break


        newPopulation = [best.copy()]

        while len(newPopulation) < populationSize:
            parent1 = selection(population, fitnessFunction, rng)
            parent2 = selection(population, fitnessFunction, rng)

            child = crossover(parent1, parent2, rng)
            child = mutate(child, mutationRate, rng)

            newPopulation.append(child)

        population = newPopulation

    bestX = int("".join(map(str, best)), 2)

    return {
        "chromosome": best,
        "x": bestX,
        "fitness": fitnessFunction(best),
        "generationsUsed": generationReached,
        "optimal": fitnessFunction(best) == optimalFitness
    }

def main():
    runs = [
        {
            "populationSize": 10,
            "chromosomeLength": 5,
            "generations": 20,
            "mutationRate": 0.1,
            "power": 2,
            "seed": None
        },
        {
            "populationSize": 20,
            "chromosomeLength": 6,
            "generations": 30,
            "mutationRate": 0.05,
            "power": 2,
            "seed": None
        },
        {
            "populationSize": 30,
            "chromosomeLength": 8,
            "generations": 50,
            "mutationRate": 0.15,
            "power": 3,
            "seed": None
        }
    ]

    results = []

    for runNumber, settings in enumerate(runs, start=1):
        print(f"\n{'=' * 40}")
        print(f"RUN {runNumber}")
        print(f"Settings: {settings}")
        print(f"{'=' * 40}")

        result = geneticAlgorithm(**settings)
        results.append(result)

        print("\nFinal Result:")
        print("Best chromosome:", result["chromosome"])
        print("Best x:", result["x"])
        print("Maximum fitness found:", result["fitness"])
        print("Generations used:", result["generationsUsed"])
        print("Optimal solution found:", result["optimal"])

    print(f"\n{'=' * 40}")
    print("SUMMARY")
    print(f"{'=' * 40}")

    for i, result in enumerate(results, start=1):
        print(
            f"Run {i}: "
            f"x = {result['x']}, "
            f"Fitness = {result['fitness']}, "
            f"Generations = {result['generationsUsed']}, "
            f"Optimal = {result['optimal']}"
        )


if __name__ == "__main__":
    main()

#Today was a very slow day at work, so I made this code randomized as an extra challenge