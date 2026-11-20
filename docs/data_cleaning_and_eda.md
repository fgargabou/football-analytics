# Documentation technique - Football Analytics

## 1. Présentation et données

Ce document retrace les principales étapes techniques du projet Football Analytics, depuis la préparation des fichiers sources jusqu'à l'exportation du dataset destiné à Power BI.

### Source des données

Les données proviennent de [Football-Data.co.uk](https://www.football-data.co.uk/).

### Périmètre de l'étude

L'analyse porte sur quatre championnats européens et cinq saisons, de 2020-2021 à 2024-2025.

| Code | Championnat | Pays |
|---|---|---|
| E0 | Premier League | Angleterre |
| D1 | Bundesliga | Allemagne |
| F1 | Ligue 1 | France |
| SP1 | La Liga | Espagne |

Au total, 20 fichiers CSV ont été utilisés, soit un fichier par championnat et par saison.

## 2. Nettoyage et contrôles des données

Une première phase de vérification a été réalisée avec Python et Pandas afin de contrôler la qualité et la cohérence des données.

Les principaux contrôles effectués :

- Vérification de la présence des championnats et des saisons attendus.
- Contrôle des plages de dates dans les fichiers.
- Recherche de valeurs négatives dans les variables numériques.
- Inspection des colonnes et des types de données.
- Vérification de la structure et de la cohérence des fichiers.
- Préparation des données pour leur regroupement.

### Anomalies et observations

**Dates et saisons :**

Lors de la vérification des fichiers, certaines plages de dates affichées semblaient incohérentes, notamment lorsque la date minimale apparaissait postérieure à la date maximale. Ce constat a nécessité une attention particulière lors de l'interprétation des dates.

**Valeurs négatives :**

Le contrôle des valeurs négatives n'a détecté aucune valeur négative dans les fichiers vérifiés.

**Types de données :**

Certaines colonnes numériques nécessitaient une attention particulière concernant leur type de données afin de permettre les calculs statistiques et leur exploitation dans Power BI.

## 3. Difficultés rencontrées et solutions

Plusieurs difficultés techniques ont été rencontrées au cours du projet.

| Difficulté | Résolution ou démarche |
|---|---|
| Organisation de plusieurs fichiers CSV | Mise en place d'une organisation par saison et par championnat |
| Vérification des dates | Contrôle des plages de dates et de leur cohérence |
| Différences de types de données | Vérification et préparation des colonnes numériques |
| Incompatibilité d'une colonne avec une mesure DAX | Correction du type de données avant d'effectuer les calculs dans Power BI |
| Création des relations entre les tables dans Power BI | Mise en place d'une table de référence des championnats et d'une relation basée sur une colonne commune |

Une difficulté particulière a été rencontrée dans Power BI : une mesure utilisant la fonction `SUM()` ne fonctionnait pas, car la colonne contenant les buts était interprétée comme du texte (`String`).

Le problème a été résolu en corrigeant le type de données de la colonne afin de permettre les opérations numériques.

## 4. Analyse exploratoire des données (EDA)

Après la préparation des données, une analyse exploratoire a été réalisée avec Pandas afin d'identifier les principales tendances et différences entre les championnats.

### 4.1. Répartition des matchs

La vérification de la distribution des matchs a permis de confirmer les volumes attendus par championnat et par saison.

| Championnat | Matchs par saison |
|---|---:|
| Premier League | 380 |
| Bundesliga | 306 |
| Ligue 1 | 380 |
| La Liga | 380 |

La différence de volume entre la Bundesliga et les autres championnats a notamment été prise en compte dans les comparaisons.

### 4.2. Moyenne de buts par championnat

L'analyse des moyennes de buts a permis d'observer des différences entre les championnats et leur évolution selon les saisons.

Pour la saison 2020-2021, les résultats obtenus étaient les suivants :

| Championnat | Moyenne de buts par match |
|---|---:|
| Bundesliga | 3,03 |
| La Liga | 2,51 |
| Ligue 1 | 2,76 |
| Premier League | 2,69 |

La Bundesliga présentait la moyenne la plus élevée parmi les quatre championnats pour cette saison.

### 4.3. Comparaison domicile / extérieur

La comparaison des performances à domicile et à l'extérieur a mis en évidence un avantage statistique pour les équipes qui jouent à domicile.

| Indicateur | Domicile | Extérieur |
|---|---:|---:|
| Moyenne de buts | 1,55 | 1,29 |
| Moyenne de tirs | 13,57 | 11,23 |
| Moyenne de tirs cadrés | 4,83 | 4,00 |
| Moyenne de corners | 5,32 | 4,38 |

Les équipes à domicile présentent des moyennes supérieures pour l'ensemble des indicateurs étudiés.

### 4.4. Principaux enseignements

Les analyses exploratoires ont notamment permis de constater que :

- Les équipes à domicile inscrivent davantage de buts en moyenne que les équipes à l'extérieur.
- Elles affichent également des moyennes supérieures en matière de tirs, de tirs cadrés et de corners.
- Les moyennes de buts varient selon les championnats et les saisons.
- Les volumes de matchs diffèrent entre la Bundesliga et les trois autres championnats.

## 5. Exportation et préparation pour Power BI

Après les différentes étapes de préparation et d'analyse, les données consolidées ont été exportées au format CSV.

Le fichier final est enregistré dans le répertoire :

`data/processed/football_matches_cleaned.csv`

Ce dataset nettoyé constitue la base de travail utilisée dans Power BI pour la modélisation des données, la création des mesures DAX et la conception du tableau de bord interactif.

Cette étape marque la transition entre le traitement des données avec Python et leur exploitation dans un environnement de Business Intelligence.
