import argparse
import pandas as pd
from config import DRAW_FILE, OUTPUT_DIR
from src.pipeline import run

def main():
    parser = argparse.ArgumentParser(description="EuroMillions Statistical Lab")
    parser.add_argument("--data", default=str(DRAW_FILE))
    parser.add_argument("--simulations", type=int, default=100_000)
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--population", type=int, default=500)
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    df, results = run(
        args.data, args.simulations, args.generations,
        args.population, args.top, args.seed
    )

    print(f"Tirages analysés : {len(df)}")
    print(f"Dernier tirage : {df.iloc[-1]['date'].date()}")
    print("\nGrilles candidates :")

    rows = []
    for rank, (score, ticket) in enumerate(results, 1):
        print(f"{rank}. {' - '.join(map(str, ticket.numbers))} | ⭐ {' - '.join(map(str, ticket.stars))} | score={score:.4f}")
        rows.append({
            "rank": rank,
            "numbers": " - ".join(map(str, ticket.numbers)),
            "stars": " - ".join(map(str, ticket.stars)),
            "score": score,
        })

    OUTPUT_DIR.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(OUTPUT_DIR / "candidates.csv", index=False)

if __name__ == "__main__":
    main()
