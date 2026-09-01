import math
import numpy as np
from .statistics import historical_targets

def consecutive_pairs(nums):
    nums = sorted(nums)
    return sum(b - a == 1 for a, b in zip(nums, nums[1:]))

def popular_pattern_penalty(nums):
    # Heuristic: discourage obvious human patterns, not winning probability.
    nums = sorted(nums)
    penalty = 0.0
    if all(n <= 31 for n in nums):
        penalty += 1.0  # date-heavy grids
    if consecutive_pairs(nums) >= 2:
        penalty += 0.8
    if len(set(n % 5 for n in nums)) <= 2:
        penalty += 0.4
    return penalty

def fitness(ticket, stats, targets, recent_weight=0.20):
    nums, stars = ticket
    nums = np.array(nums)
    stars = np.array(stars)

    freq = stats["freq"].reindex(nums).to_numpy(dtype=float)
    freq_score = (freq.mean() - stats["freq"].mean()) / (stats["freq"].std() or 1)

    recent = stats["recent"].reindex(nums).to_numpy(dtype=float)
    recent_score = (recent.mean() - stats["recent"].mean()) / (stats["recent"].std() or 1)

    total = nums.sum()
    sum_score = -abs(total - targets["sum_mean"]) / targets["sum_std"]

    odd = np.sum(nums % 2)
    parity_score = -abs(odd - targets["odd_mean"])

    low = np.sum(nums <= 25)
    low_score = -abs(low - targets["low_mean"])

    decade_count = len(set((nums - 1) // 10))
    diversity_score = (decade_count - 3) * 0.4

    star_freq = stats["star_freq"].reindex(stars).mean()
    star_score = (star_freq - stats["star_freq"].mean()) / (stats["star_freq"].std() or 1)

    penalty = popular_pattern_penalty(nums)

    return (
        0.25 * freq_score
        + recent_weight * recent_score
        + 0.15 * sum_score
        + 0.10 * parity_score
        + 0.10 * low_score
        + 0.10 * diversity_score
        + 0.10 * star_score
        - 0.20 * penalty
    )
