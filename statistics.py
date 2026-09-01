from collections import Counter
import numpy as np
import pandas as pd

def number_frequencies(df):
    c = Counter()
    for _, r in df.iterrows():
        c.update(int(r[f"n{i}"]) for i in range(1, 6))
    return pd.Series({n: c[n] for n in range(1, 51)})

def star_frequencies(df):
    c = Counter()
    for _, r in df.iterrows():
        c.update(int(r[f"s{i}"]) for i in range(1, 3))
    return pd.Series({n: c[n] for n in range(1, 13)})

def last_draws(df, n=5):
    return df.sort_values("date").tail(n)

def recent_frequency(df, n=5):
    return number_frequencies(last_draws(df, n))

def number_delays(df):
    ordered = df.sort_values("date")
    last_seen = {n: None for n in range(1, 51)}
    for idx, (_, r) in enumerate(ordered.iterrows()):
        for i in range(1, 6):
            last_seen[int(r[f"n{i}"])] = idx
    end = len(ordered) - 1
    return pd.Series({n: end - last_seen[n] if last_seen[n] is not None else len(ordered)
                      for n in range(1, 51)})

def draw_features(numbers):
    numbers = np.asarray(numbers)
    return {
        "sum": int(numbers.sum()),
        "odd": int(np.sum(numbers % 2)),
        "low": int(np.sum(numbers <= 25)),
        "decades": tuple(int((n-1)//10) for n in numbers),
    }

def historical_targets(df):
    nums = df[[f"n{i}" for i in range(1,6)]].sum(axis=1)
    odd = df[[f"n{i}" for i in range(1,6)]].apply(lambda x: (x % 2).sum(), axis=1)
    return {
        "sum_mean": float(nums.mean()),
        "sum_std": float(nums.std(ddof=0) or 1),
        "odd_mean": float(odd.mean()),
        "low_mean": float(df[[f"n{i}" for i in range(1,6)]].apply(lambda x: (x <= 25).sum(), axis=1).mean()),
    }
