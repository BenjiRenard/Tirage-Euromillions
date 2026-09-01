from pathlib import Path
import pandas as pd

REQUIRED = ["date", "n1", "n2", "n3", "n4", "n5", "s1", "s2"]

def load_draws(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    df = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")

    df = df[REQUIRED].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    for c in REQUIRED[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna().drop_duplicates("date").sort_values("date").reset_index(drop=True)

    for _, row in df.iterrows():
        nums = [int(row[f"n{i}"]) for i in range(1, 6)]
        stars = [int(row[f"s{i}"]) for i in range(1, 3)]
        if len(set(nums)) != 5 or not all(1 <= n <= 50 for n in nums):
            raise ValueError(f"Tirage invalide : {row.to_dict()}")
        if len(set(stars)) != 2 or not all(1 <= s <= 12 for s in stars):
            raise ValueError(f"Etoiles invalides : {row.to_dict()}")

    return df

def historical_keys(df: pd.DataFrame) -> set[tuple]:
    return {
        (
            tuple(sorted(int(row[f"n{i}"]) for i in range(1, 6))),
            tuple(sorted(int(row[f"s{i}"]) for i in range(1, 3))),
        )
        for _, row in df.iterrows()
    }
