import random
from .models import Ticket

def random_ticket(rng):
    nums = tuple(sorted(rng.sample(range(1, 51), 5)))
    stars = tuple(sorted(rng.sample(range(1, 13), 2)))
    return Ticket(nums, stars)

def mutate(ticket, rng, probability=0.12):
    nums = list(ticket.numbers)
    stars = list(ticket.stars)

    if rng.random() < probability:
        idx = rng.randrange(5)
        available = [n for n in range(1, 51) if n not in nums]
        nums[idx] = rng.choice(available)

    if rng.random() < probability:
        idx = rng.randrange(2)
        available = [s for s in range(1, 13) if s not in stars]
        stars[idx] = rng.choice(available)

    return Ticket(tuple(sorted(nums)), tuple(sorted(stars)))

def crossover(a, b, rng):
    nums_pool = list(dict.fromkeys(a.numbers + b.numbers))
    stars_pool = list(dict.fromkeys(a.stars + b.stars))

    if len(nums_pool) < 5:
        return a
    if len(stars_pool) < 2:
        return a

    nums = tuple(sorted(rng.sample(nums_pool, 5)))
    stars = tuple(sorted(rng.sample(stars_pool, 2)))
    return Ticket(nums, stars)

def evolve(initial_population, score_fn, generations=200, elite_size=100,
           population_size=1000, mutation_rate=0.12, seed=42):
    rng = random.Random(seed)
    population = list(initial_population)

    while len(population) < population_size:
        population.append(random_ticket(rng))

    for _ in range(generations):
        scored = sorted(((score_fn(t), t) for t in population), reverse=True, key=lambda x: x[0])
        elites = [t for _, t in scored[:elite_size]]
        population = elites.copy()

        while len(population) < population_size:
            a = rng.choice(elites)
            b = rng.choice(elites)
            child = crossover(a, b, rng)
            child = mutate(child, rng, mutation_rate)
            population.append(child)

    return sorted(((score_fn(t), t) for t in population), reverse=True, key=lambda x: x[0])
