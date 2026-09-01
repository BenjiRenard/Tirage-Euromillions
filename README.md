# EuroMillions Statistical Lab

Projet de Data Science en Python consacré à l'analyse historique et à la génération expérimentale de grilles EuroMillions.

Le projet combine :

- analyse statistique des tirages historiques ;
- fréquences et récence ;
- contraintes de parité, somme et répartition par dizaines ;
- Monte Carlo pour générer un grand ensemble de candidats ;
- algorithme génétique pour optimiser une fonction de fitness ;
- pénalisation de certains motifs humains très évidents ;
- interface Streamlit ;
- export des candidats en CSV.

> **Important :** ce projet ne prédit pas les tirages et n'augmente pas mathématiquement les chances de gagner. Les critères servent à explorer et classer des combinaisons selon des hypothèses statistiques et comportementales.

## Structure

```text
euromillions-ai/
├── data/
│   └── draws.csv
├── src/
│   ├── data_loader.py
│   ├── fitness.py
│   ├── genetic_algorithm.py
│   ├── models.py
│   ├── monte_carlo.py
│   ├── pipeline.py
│   └── statistics.py
├── tests/
├── dashboard.py
├── main.py
├── config.py
├── requirements.txt
└── .gitignore
```

## Installation

Python 3.11+ recommandé.

```bash
git clone <URL_DU_REPO>
cd euromillions-ai

python -m venv .venv
```

Windows :

```bash
.venv\Scripts\activate
```

Linux/macOS :

```bash
source .venv/bin/activate
```

Puis :

```bash
pip install -r requirements.txt
```

## Exécution

Simulation locale :

```bash
python main.py --simulations 100000 --generations 100 --population 500 --top 3
```

Pour une simulation plus importante :

```bash
python main.py --simulations 1000000 --generations 200 --population 1000 --top 10
```

Interface graphique :

```bash
streamlit run dashboard.py
```

## Données

Le dépôt contient une version normalisée de l'historique utilisé pour le développement :

```text
date,n1,n2,n3,n4,n5,s1,s2
```

Le chargeur accepte uniquement ce format normalisé.

## Pipeline

```text
Historique
    │
    ▼
Nettoyage / validation
    │
    ▼
Statistiques
    │
    ├── fréquences
    ├── récence
    ├── parité
    ├── sommes
    └── dizaines
    │
    ▼
Monte Carlo
    │
    ▼
Population candidate
    │
    ▼
Algorithme génétique
    │
    ├── sélection
    ├── croisement
    └── mutation
    │
    ▼
Fitness
    │
    ▼
Top N grilles
```

## Reproductibilité

Le paramètre `--seed` permet de reproduire une simulation :

```bash
python main.py --seed 42


MIT.
