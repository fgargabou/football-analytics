import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==================================================
# 1. CHARGEMENT DU DATASET
# ==================================================

DATA_FILE = Path("data/processed/football_matches_cleaned.csv")

football_df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

print("\nDataset loaded successfully!")
print("Shape:", football_df.shape)

print("\nFirst 5 rows:")
print(football_df.head())

# ==================================================
# 2. VUE D'ENSEMBLE DU DATASET
# ==================================================

print("\n========== DATASET INFORMATION ==========")
football_df.info()

print("\n========== MISSING VALUES ==========")
missing_values = football_df.isnull().sum()
missing_values = missing_values[missing_values > 0].sort_values(ascending=False)

print(missing_values)

print("\n========== BASIC STATISTICS ==========")
print(football_df[["FTHG", "FTAG", "HTHG", "HTAG"]].describe())

# ==================================================
# 3. CREATION DES INDICATEURS
# ==================================================

# Nombre total de buts par match
football_df["TotalGoals"] = football_df["FTHG"] + football_df["FTAG"]

# Différence de buts entre domicile et extérieur
football_df["GoalDifference"] = football_df["FTHG"] - football_df["FTAG"]

# Résultat du match en toutes lettres
result_mapping = {
    "H": "Home Win",
    "D": "Draw",
    "A": "Away Win"
}

football_df["Result"] = football_df["FTR"].map(result_mapping)

print("\n========== NEW INDICATORS ==========")
print(football_df[[
    "HomeTeam", "AwayTeam",
    "FTHG", "FTAG",
    "TotalGoals", "GoalDifference", "Result"
]].head(10))

# ==================================================
# 4. ANALYSE GLOBALE DES BUTS
# ==================================================

print("\n========== GLOBAL GOALS ANALYSIS ==========")

print("Total goals :", football_df["TotalGoals"].sum())

print("Average goals per match :", round(football_df["TotalGoals"].mean(), 2))

print("Average home goals :", round(football_df["FTHG"].mean(), 2))

print("Average away goals :", round(football_df["FTAG"].mean(), 2))

# Match avec le plus grand nombre de buts
highest_scoring_match = football_df.loc[football_df["TotalGoals"].idxmax()] # récupérer l'indice correspondant à la valeur maximale


print("\nHighest scoring match:")
print(
    highest_scoring_match["HomeTeam"],
    "vs",
    highest_scoring_match["AwayTeam"]
)
print("Score :", highest_scoring_match["FTHG"], "-", highest_scoring_match["FTAG"])
print("Total goals :", highest_scoring_match["TotalGoals"])

# ==================================================
# 5. ANALYSE DES BUTS PAR CHAMPIONNAT
# ==================================================

# comparer les quatre championnats pour identifier celui qui produit le plus de buts
# on compare des moyennes sur 5 saisons
goals_by_league = football_df.groupby("League").agg( # .agg() : appliquer plusieurs calculs sur chaque groupe
    TotalGoals=("TotalGoals", "sum"),
    AverageGoals=("TotalGoals", "mean"),
    HomeGoals=("FTHG", "mean"),
    AwayGoals=("FTAG", "mean"),
    TotalMatches=("TotalGoals", "count")
).round(2) # arrondir les nombres à 2 chiffres après la virgule

goals_by_league = goals_by_league.sort_values(by="AverageGoals",ascending=False)

print("\n========== GOALS BY LEAGUE ==========")
print(goals_by_league)

# ==================================================
# 6. REPARTITION DES RESULTATS PAR CHAMPIONNAT
# ==================================================

# pour chaque championnat on détermine le % de victoires HOME et AWAY, et de matchs nuls
results_by_league = pd.crosstab( # croise deux variables
    football_df["League"],
    football_df["Result"],
    normalize="index"
) * 100

results_by_league = results_by_league.round(2)

print("\n========== RESULTS DISTRIBUTION BY LEAGUE ==========")
print(results_by_league)

# ==================================================
# 7. EVOLUTION DES BUTS PAR SAISON
# ==================================================

goals_by_season = football_df.groupby("Season").agg( # .agg() : appliquer plusieurs calculs sur chaque groupe
    TotalGoals=("TotalGoals", "sum"),
    AverageGoals=("TotalGoals", "mean"),
    TotalMatches=("TotalGoals", "count")
).round(2)

print("\n========== GOALS BY SEASON ==========")
print(goals_by_season)

# ==================================================
# 8. COMPARAISON DES BUTS PAR CHAMPIONNAT ET SAISON
# ==================================================

goals_league_season = football_df.pivot_table( # créer un tableau croisé dynamique
    index="Season",
    columns="League",
    values="TotalGoals",
    aggfunc="mean"
).round(2)

print("\n========== AVERAGE GOALS BY LEAGUE AND SEASON ==========")
print(goals_league_season)

# ==================================================
# 9. PERFORMANCES DES EQUIPES
# ==================================================

######## 9.1 Top 10 des équipes par buts marqués

# Calcul des buts marqués à domicile et à l'extérieur
home_goals = football_df.groupby("HomeTeam")["FTHG"].sum()
away_goals = football_df.groupby("AwayTeam")["FTAG"].sum()

# Regroupement des buts marqués par équipe
team_goals = home_goals.add(away_goals, fill_value=0)

# Classement des 10 équipes les plus prolifiques
top_10_goals = team_goals.sort_values(ascending=False).head(10)

print("\n========== TOP 10 TEAMS BY GOALS SCORED ==========")
print(top_10_goals)

######## 9.2 Top 10 des équipes par nombre de victoires

# Classement des victoires par équipe

home_wins = football_df[football_df["FTR"] == "H"].groupby("HomeTeam").size()
away_wins = football_df[football_df["FTR"] == "A"].groupby("AwayTeam").size()

team_wins = home_wins.add(away_wins, fill_value=0)

top_10_wins = team_wins.sort_values(ascending=False).head(10)

print("\n========== TOP 10 TEAMS BY WINS ==========")
print(top_10_wins)

# ==================================================
# 10. ANALYSE DES STATISTIQUES DES MATCHS
# ==================================================

# Comparaison des statistiques des matchs
match_stats = pd.DataFrame({
    "Home": [
        football_df["HS"].mean(),
        football_df["HST"].mean(),
        football_df["HC"].mean()
    ],
    "Away": [
        football_df["AS"].mean(),
        football_df["AST"].mean(),
        football_df["AC"].mean()
    ]
}, index=["Shots", "Shots on Target", "Corners"]).round(2)

print("\n========== HOME VS AWAY MATCH STATISTICS ==========")
print(match_stats)