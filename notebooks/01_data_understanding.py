
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==================================================
# 1. COLLECTE DE DONNÉES
# ==================================================

# Localisation des fichiers
DATA_PATH = Path("data/raw") # indique où se trouve les données
files = sorted(DATA_PATH.glob("*/*.csv")) # cherche les fichiers csv dans les dossiers de saisons

print(f"Number of CSV files found: {len(files)}")


# ==================================================
# 2. CHARGEMENT ET PRÉSENTATION DES DONNÉES
# ==================================================

# Charger le premier fichier csv
df = pd.read_csv(files[0], encoding="latin-1")

# Afficher le nom du premier fichier
print("\n========== DATASET OVERVIEW ==========")
print("File:", files[0].name)

# Afficher les dimensions du dataset
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

# Afficher les 5 premières lignes
print("\nFirst 5 rows:")
print(df.head().to_string())

# Afficher les informations du dataset
print("\nDataset information:")
df.info()

# Afficher les noms des colonnes
print("\nDataset columns:")
print(df.columns.tolist())


# ==================================================
# 3. ANALYSE DES VALEURS MANQUANTES
# ==================================================

# Vérifier les valeurs manquantes
print("\n========== MISSING VALUES ==========")
missing_values = df.isnull().sum().sort_values(ascending=False)
print(missing_values[missing_values > 0])


# ==================================================
# 4. STATISTIQUES DESCRIPTIVES
# ==================================================

# Les statistiques principales
print("\n========== DESCRIPTIVE STATISTICS ==========")

print(df[["FTHG", "FTAG", "HS", "AS", "HST", "AST", "HC", "AC"]].describe())

# FTHG : nombre de buts marqués par l'équipe à domicile
# FTAG : nombre de buts marqués par l'équipe à l'extérieur
# HS : nombre total de tirs de l'équipe à domicile
# AS : nombre total de tirs de l'équipe à l'extérieur
# HST : nombre de tirs cadrés de l'équipe à domicile
# AST : nombre de tirs cadrés de l'équipe à l'extérieur
# HC : nombre de corners de l'équipe à domicile
# AC : nombre de corners de l'équipe à l'extérieur


# ==================================================
# 5. ANALYSE DES ÉQUIPES ET DES RÉSULTATS
# ==================================================

# Comprendre quelles équipes et quels résultats sont présents
teams = set(df["HomeTeam"].unique()).union(set(df["AwayTeam"].unique()))

print("\n========== TEAMS AND MATCH RESULTS ==========")

print("Number of unique teams:", len(teams))
print("Teams:", sorted(teams))

print("\nMatch results:")
print(df["FTR"].value_counts()) # FTR : FULL TIME RESULT : résultat du match

# Nombre d'équipes à domicile
print("\nNumber of home teams:", df["HomeTeam"].nunique()) # compte le nombre de valeurs différentes

# Valeurs possibles du résultat final
print("Match results:", df["FTR"].unique()) # affiche les valeurs distinctes


# ==================================================
# 6. VÉRIFICATION DES DOUBLONS
# ==================================================

# Vérifier si des matchs apparaissent plusieurs fois
print("\n========== DUPLICATE CHECK ==========")
print("Number of duplicate rows:", df.duplicated().sum())


# ==================================================
# 7. VÉRIFICATION DE LA COHÉRENCE DES DONNÉES
# ==================================================

print("\n========== DATA CONSISTENCY ==========")

# Vérifier les scores négatifs (vérifie si les buts sont négatifs et compte le nombre de fois où cette condition est vraie)
print("Negative home goals:", (df["FTHG"] < 0).sum())
print("Negative away goals:", (df["FTAG"] < 0).sum())

# Vérifier les résultats des matchs
expected_result = np.select(
    [
        df["FTHG"] > df["FTAG"],
        df["FTHG"] == df["FTAG"]
    ],
    ["H", "D"],
    default="A"
)

print(
    "Inconsistent match results:",
    (df["FTR"] != expected_result).sum()
)
# On a comparé les scores avec la colonne FTR

# Vérifier les valeurs manquantes dans les colonnes essentielles
print("\nMissing values in essential columns:")
print(df[["FTHG", "FTAG", "FTR"]].isnull().sum())


# ==================================================
# 8. COMPARAISON DE LA STRUCTURE DES 20 FICHIERS
# ==================================================

print("\n========== FILE STRUCTURE COMPARISON ==========")

# Comparer le nombre de colonnes de chaque fichier
for file in files :
    temp_df = pd.read_csv(file, encoding="latin-1")

    print(
        f"{file.parent.name} | {file.name} | "
        f"{temp_df.shape[0]} rows | {temp_df.shape[1]} columns"
    )


# ==================================================
# 9. IDENTIFICATION DES DIFFÉRENCES ENTRE LES COLONNES
# ==================================================

print("\n========== COLUMN COMPARISON ==========")

# Utiliser le premier fichier comme référence
reference_df = pd.read_csv(files[0], encoding="latin-1")
reference_columns = set(reference_df.columns)

# comparer les noms des colonnes de chaque fichier avec ceux du premier fichier
for file in files:

    temp_df = pd.read_csv(file, encoding="latin-1")
    current_columns = set(temp_df.columns)

    # Identifier les colonnes supplémentaires
    extra_columns = current_columns - reference_columns

    # Identifier les colonnes manquantes
    missing_columns = reference_columns - current_columns

    if extra_columns or missing_columns:

        print(f"\nFile: {file.parent.name}/{file.name}")

        print("Extra columns:", sorted(extra_columns))
        print("Missing columns:", sorted(missing_columns))

    else:
        print(f"{file.parent.name}/{file.name}: Same columns")

# ==================================================
# 10. NORMALISATION DES NOMS DE COLONNES
# ==================================================

import unicodedata

print("\n========== COLUMN NAME NORMALIZATION ==========")

# ==================================================
# 10. NORMALISATION DES NOMS DE COLONNES
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
# 11. VERIFICATION APRES NORMALISATION
# ==================================================

for file in files:

    temp_df = pd.read_csv(file, encoding="latin-1")
    temp_df = normalize_columns(temp_df)

    if "Div" in temp_df.columns:
        print(f"{file.parent.name}/{file.name}: Div OK")
    else:
        print(f"{file.parent.name}/{file.name}: Div MISSING")

# ==================================================
# 12. COMPARAISON DES COLONNES APRES NORMALISATION
# ==================================================

print("\n========== COLUMN COMPARISON AFTER NORMALIZATION ==========")

reference_df = pd.read_csv(files[0], encoding="latin-1")
reference_df = normalize_columns(reference_df)

reference_columns = set(reference_df.columns)

for file in files:

    temp_df = pd.read_csv(file, encoding="latin-1")
    temp_df = normalize_columns(temp_df)

    current_columns = set(temp_df.columns)

    extra_columns = current_columns - reference_columns
    missing_columns = reference_columns - current_columns

    if extra_columns or missing_columns:

        print(f"\nFile: {file.parent.name}/{file.name}")
        print("Extra columns:", sorted(extra_columns))
        print("Missing columns:", sorted(missing_columns))

    else:
        print(f"{file.parent.name}/{file.name}: Same columns")

# ==================================================
# 13. VERIFICATION DES LIGUES ET DES SAISONS
# ==================================================

print("\n========== LEAGUE AND SEASON VERIFICATION ==========")

for file in files:

    temp_df = pd.read_csv(file, encoding="latin-1")
    temp_df = normalize_columns(temp_df)

    # Convertir les dates en format datetime
    temp_df["Date"] = pd.to_datetime(
        temp_df["Date"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    print(
        f"File: {file.parent.name}/{file.name} | "
        f"League: {temp_df['Div'].unique()} | "
        f"Dates: {temp_df['Date'].min().strftime('%d/%m/%Y')} "
        f"- {temp_df['Date'].max().strftime('%d/%m/%Y')}"
    )

# ========================================================================
# 14. VERIFICATION DES VALEURS MANQUANTES DANS LES COLONNES ESSENTIELLES
# ========================================================================

print("\n========== ESSENTIAL DATA COMPLETENESS ==========")

essential_columns = ["Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR"]

for file in files:
    temp_df = pd.read_csv(file, encoding="latin-1")
    temp_df = normalize_columns(temp_df)

    missing = temp_df[essential_columns].isnull().sum().sum()

    print(
        f"{file.parent.name}/{file.name} | "
        f"Missing essential values: {missing}"
    )