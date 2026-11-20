
import pandas as pd
import numpy as np
from pathlib import Path

# ==================================================
# 1. LOCALISATION DES FICHIERS
# ==================================================

DATA_PATH = Path("data/raw")

files = sorted(DATA_PATH.glob("*/*.csv"))

print("Number of CSV files found:", len(files))


# ==================================================
# 2. NORMALISATION DES NOMS DE COLONNES
# ==================================================

def normalize_columns(dataframe):

    normalized_columns = []

    for column in dataframe.columns:

        column = str(column)

        # Supprimer le BOM mal interprété
        if column.startswith("ï»¿"):
            column = column[3:]

        # Supprimer un éventuel BOM correctement interprété
        elif column.startswith("\ufeff"):
            column = column[1:]

        normalized_columns.append(column.strip())
    dataframe.columns = normalized_columns
    return dataframe


# ==================================================
# 3. CHARGEMENT DES 20 FICHIERS
# ==================================================

datasets = {}

for file in files:

    temp_df = pd.read_csv(file, encoding="latin-1")

    # Normaliser les noms de colonnes
    temp_df = normalize_columns(temp_df)

    # Enregistrer le DataFrame dans le dictionnaire
    datasets[str(file)] = temp_df

print("Number of datasets loaded:", len(datasets))

# ==================================================
# 4. VERIFICATION DES DIMENSIONS DES DATASETS
# ==================================================

print("\n========== DATASETS DIMENSIONS ==========")

for file_name, dataframe in datasets.items():
    print(
        f"{file_name} | "
        f"Rows: {dataframe.shape[0]} | "
        f"Columns: {dataframe.shape[1]}"
    )


# ==================================================
# 5. VERIFICATION DES DOUBLONS
# ==================================================

print("\n========== DUPLICATE CHECK ==========")

total_duplicates = 0 # accumulateur

for file_name, dataframe in datasets.items():

    duplicates = dataframe.duplicated().sum()

    total_duplicates += duplicates 

    print(f"{file_name} | Duplicate rows: {duplicates}")

print("\nTotal duplicate rows:", total_duplicates)


# ==================================================
# 6. VERIFICATION DES VALEURS NEGATIVES
# ==================================================

print("\n========== NEGATIVE VALUES CHECK ==========")

stat_columns = ["FTHG", "FTAG", "HTHG", "HTAG","HS", "AS", "HST", "AST","HC", "AC", "HF", "AF","HY", "AY", "HR", "AR"] # liste des colonnes à contrôler
# FTHG, FTAG : buts en fin de match
# HTHG, HTAG : buts à la mi-temps
# HS, AS : tirs
# HST, AST : tirs cadrés
# HC, AC : corners
# HF, AF : fautes
# HY, AY : cartons jaunes
# HR, AR : cartons rouges

total_negative_values = 0 # compteur global pour les 20 fichiers

for file_name, dataframe in datasets.items():

    # Compter les valeurs négatives dans chaque colonne
    negative_by_column = dataframe[stat_columns].lt(0).sum() # lt(0) : less than 0

    # Calculer le nombre total de valeurs négatives du fichier
    negative_total = negative_by_column.sum()

    total_negative_values += negative_total

    if negative_total > 0:
        print(f"\n{file_name}")
        print(negative_by_column[negative_by_column > 0])

    else:
        print(f"{file_name} | No negative values")

print("\nTotal negative values:", total_negative_values)

# ==================================================
# 7. VERIFICATION DE LA COHERENCE DES RESULTATS
# ==================================================

print("\n========== MATCH RESULTS CONSISTENCY CHECK ==========")

total_inconsistent_results = 0

for file_name, dataframe in datasets.items():

    # Déterminer le résultat attendu à partir des scores
    expected_result = np.select(
        [
            dataframe["FTHG"] > dataframe["FTAG"],
            dataframe["FTHG"] == dataframe["FTAG"]
        ],
        ["H", "D"],
        default="A"
    )

    # Comparer le résultat attendu avec le résultat enregistré
    inconsistent_results = dataframe["FTR"] != expected_result

    # Compter les résultats incohérents
    inconsistent_count = inconsistent_results.sum()

    total_inconsistent_results += inconsistent_count

    if inconsistent_count > 0:

        print(f"\n{file_name}")
        print(dataframe.loc[inconsistent_results, ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]])

    else:

        print(f"{file_name} | All results are consistent")

print("\nTotal inconsistent results:", total_inconsistent_results)

# ==================================================
# 8. VERIFICATION DES VALEURS MANQUANTES
# ==================================================

print("\n========== MISSING VALUES CHECK ==========")

total_missing_values = 0

for file_name, dataframe in datasets.items():

    # Compter les valeurs manquantes par colonne
    missing_by_column = dataframe.isnull().sum()

    # Calculer le nombre total de valeurs manquantes
    missing_total = missing_by_column.sum()

    total_missing_values += missing_total

    if missing_total > 0:

        print(f"\n{file_name}")
        print(missing_by_column[missing_by_column > 0])

    else:

        print(f"{file_name} | No missing values")

print("\nTotal missing values:", total_missing_values)

# ==================================================
# 9. INSPECTION DES STATISTIQUES MANQUANTES
# ==================================================

print("\n========== MISSING MATCH STATISTICS ==========")

stat_columns = [
    "FTHG", "FTAG", "HTHG", "HTAG",
    "HS", "AS", "HST", "AST",
    "HC", "AC", "HF", "AF",
    "HY", "AY", "HR", "AR"
]

for file_name, dataframe in datasets.items():

    # Identifier les matchs ayant au moins une statistique manquante
    missing_rows = dataframe[stat_columns].isnull().any(axis=1)

    if missing_rows.any():

        print(f"\n{file_name}")

        print(
            dataframe.loc[
                missing_rows,
                ["Date", "HomeTeam", "AwayTeam"] + stat_columns
            ]
        )

# ==================================================
# 10. VERIFICATION DES STATISTIQUES INCOHERENTES
# ==================================================

print("\n========== INCONSISTENT MATCH STATISTICS ==========")

total_inconsistencies = 0

for file_name, dataframe in datasets.items():

    # Vérifier les incohérences statistiques
    invalid_rows = (
        (dataframe["HST"] > dataframe["HS"]) |
        (dataframe["AST"] > dataframe["AS"]) |
        (dataframe["HTHG"] > dataframe["FTHG"]) |
        (dataframe["HTAG"] > dataframe["FTAG"])
    )

    inconsistency_count = invalid_rows.sum()
    total_inconsistencies += inconsistency_count

    if inconsistency_count > 0:

        print(f"\n{file_name}")

        print(
            dataframe.loc[
                invalid_rows,
                ["Date", "HomeTeam", "AwayTeam",
                 "FTHG", "FTAG", "HTHG", "HTAG",
                 "HS", "AS", "HST", "AST"]
            ]
        )

    else:

        print(f"{file_name} | No inconsistencies")

print("\nTotal inconsistent matches:", total_inconsistencies)

# ==================================================
# 11. VERIFICATION DES DOUBLONS DE MATCHS
# ==================================================

print("\n========== DUPLICATE MATCHES CHECK ==========")

total_duplicate_matches = 0

for file_name, dataframe in datasets.items():

    # Un match est identifié par sa date et ses deux équipes
    duplicate_matches = dataframe.duplicated(
        subset=["Date", "HomeTeam", "AwayTeam"]
    )

    duplicate_count = duplicate_matches.sum()
    total_duplicate_matches += duplicate_count

    if duplicate_count > 0:

        print(f"\n{file_name}")

        print(
            dataframe.loc[
                duplicate_matches,
                ["Date", "HomeTeam", "AwayTeam"]
            ]
        )

    else:

        print(f"{file_name} | No duplicate matches")

print("\nTotal duplicate matches:", total_duplicate_matches)

# ==================================================
# 12. CONVERSION DES DATES
# ==================================================

print("\n========== DATE CONVERSION ==========")

for file_name, dataframe in datasets.items():

    # Convertir les dates au format datetime
    dataframe["Date"] = pd.to_datetime(
        dataframe["Date"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    invalid_dates = dataframe["Date"].isna().sum()

    if invalid_dates > 0:
        print(f"{file_name} | Invalid dates: {invalid_dates}")

    else:
        print(f"{file_name} | Dates converted successfully")

# ==================================================
# 14. AJOUT DES COLONNES SEASON ET LEAGUE
# ==================================================

league_names = {
    "D1": "Bundesliga",
    "E0": "Premier League",
    "F1": "Ligue 1",
    "SP1": "La Liga"
}

season_names = {
    "2021": "2020-2021",
    "2122": "2021-2022",
    "2223": "2022-2023",
    "2324": "2023-2024",
    "2425": "2024-2025"
}

for file_name, dataframe in datasets.items():

    # Récupérer le dossier de saison et le code du championnat
    file_path = Path(file_name)

    season_code = file_path.parent.name
    league_code = file_path.stem.split(" ")[0]

    dataframe["Season"] = season_names[season_code]
    dataframe["League"] = league_names[league_code]

print("Season and League columns added successfully!")

# ==================================================
# 15. FUSION DES 20 DATASETS
# ==================================================

# Fusionner tous les DataFrames
football_df = pd.concat(datasets.values(), ignore_index=True)

print("========== MERGED DATASET ==========")

print("Total matches:", football_df.shape[0])
print("Total columns:", football_df.shape[1])

print("\nMatches by league:")
print(football_df["League"].value_counts())

print("\nMatches by season:")
print(football_df["Season"].value_counts())

print("\nDataset preview:")
print(football_df.head())

# ==================================================
# 16. VERIFICATION DE LA REPARTITION DES MATCHS
# ==================================================

print("\n========== MATCHES DISTRIBUTION ==========")

distribution = pd.crosstab(
    football_df["Season"],
    football_df["League"]
)

print(distribution)

print("\nTotal matches:", distribution.sum().sum())

# ==================================================
# 17. EXPORT DU DATASET FINAL
# ==================================================

# Créer le dossier de destination s'il n'existe pas
OUTPUT_PATH = Path("data/processed")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Enregistrer le dataset fusionné
football_df.to_csv(
    OUTPUT_PATH / "football_matches_cleaned.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Dataset exported successfully!")
print("File:", OUTPUT_PATH / "football_matches_cleaned.csv")

# ==================================================
# 18. VERIFICATION DU DATASET EXPORTE
# ==================================================

OUTPUT_FILE = Path("data/processed/football_matches_cleaned.csv")

# Recharger le fichier exporté
football_check = pd.read_csv(OUTPUT_FILE)

print("\n========== EXPORTED DATASET VALIDATION ==========")

print("Rows:", football_check.shape[0])
print("Columns:", football_check.shape[1])

print("\nMissing Season:", football_check["Season"].isna().sum())
print("Missing League:", football_check["League"].isna().sum())

print("\nLeagues:", football_check["League"].nunique())
print("Seasons:", football_check["Season"].nunique())

print("\nExport validation completed!")