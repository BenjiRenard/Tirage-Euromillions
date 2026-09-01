import numpy as np
from .models import Ticket

def generate_candidates(n_simulations, historical_keys, rng=None, batch_size=100_000):
    rng = rng or np.random.default_rng()
    candidates = []
    seen = set()

    remaining = n_simulations
    while remaining > 0:
        batch = min(batch_size, remaining)
        for _ in range(batch):
            nums = tuple(sorted(rng.choice(50, 5, replace=False) + 1))
            stars = tuple(sorted(rng.choice(12, 2, replace=False) + 1))
            key = (nums, stars)
            if key not in historical_keys and key not in seen:
                seen.add(key)
                candidates.append(Ticket(nums, stars))
        remaining -= batch

    return candidates
