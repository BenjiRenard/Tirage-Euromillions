from .data_loader import load_draws, historical_keys
from .statistics import number_frequencies, star_frequencies, recent_frequency, historical_targets
from .fitness import fitness
from .monte_carlo import generate_candidates
from .genetic_algorithm import evolve

def build_stats(df, recent_draws=5):
    return {
        "freq": number_frequencies(df),
        "star_freq": star_frequencies(df),
        "recent": recent_frequency(df, recent_draws),
    }

def run(path, simulations=100_000, generations=100, population_size=500,
        top_n=3, seed=42):
    df = load_draws(path)
    historical = historical_keys(df)
    stats = build_stats(df)
    targets = historical_targets(df)

    candidates = generate_candidates(simulations, historical, rng=__import__("numpy").random.default_rng(seed))

    score_fn = lambda t: fitness(t.key(), stats, targets)
    evolved = evolve(
        candidates[:min(len(candidates), population_size)],
        score_fn,
        generations=generations,
        population_size=population_size,
        seed=seed,
    )

    results = []
    seen = set()
    for score, ticket in evolved:
        if ticket.key() in historical or ticket.key() in seen:
            continue
        seen.add(ticket.key())
        results.append((score, ticket))
        if len(results) >= top_n:
            break

    return df, results
