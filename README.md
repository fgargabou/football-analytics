# Football Analytics - Analyse des performances des championnats européens

## 1. Présentation du projet

Ce projet porte sur l'analyse des performances de quatre grands championnats européens de football sur plusieurs saisons, de 2020 à 2024.

L'objectif est de mettre en pratique différentes techniques d'analyse de données, depuis la collecte et le nettoyage des données avec Python jusqu'à leur exploitation et leur visualisation dans Power BI.

Le projet combine programmation, analyse exploratoire et Business Intelligence afin de transformer des données brutes de matchs en informations exploitables à travers un tableau de bord interactif.

## 2. Objectifs

Les principaux objectifs de ce projet sont :

- Collecter et regrouper des données issues de plusieurs championnats européens.
- Nettoyer et préparer les données afin de garantir leur cohérence et leur fiabilité.
- Réaliser une analyse exploratoire pour identifier des tendances et des relations entre les différentes variables.
- Comparer les performances des équipes à domicile et à l'extérieur.
- Étudier l'évolution des statistiques entre les championnats et les saisons.
- Concevoir des indicateurs de performance à l'aide de DAX.
- Développer un tableau de bord interactif avec Power BI pour faciliter l'exploration des résultats.

## 3. Championnats et période étudiés

L'étude porte sur quatre championnats européens :

| Code | Championnat | Pays |
|---|---|---|
| E0 | Premier League | Angleterre |
| D1 | Bundesliga | Allemagne |
| SP1 | La Liga | Espagne |
| F1 | Ligue 1 | France |

**Période d'étude :** saisons 2020-2021 à 2024-2025.

Les données comprennent notamment les résultats des matchs ainsi que différentes statistiques relatives aux performances des équipes.

## 4. Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python | Traitement et analyse des données |
| Pandas | Manipulation, nettoyage et exploration des données |
| NumPy | Opérations et calculs numériques |
| Matplotlib | Création de visualisations |
| Seaborn | Analyse graphique et visualisation statistique |
| Power BI | Modélisation et création du tableau de bord |
| DAX | Création de mesures et d'indicateurs de performance |

## 5. Collecte et préparation des données

5. Collecte et préparation des données

## 5. Collecte et préparation des données

Les données utilisées dans ce projet proviennent de [Football-Data.co.uk](https://www.football-data.co.uk/), une plateforme mettant à disposition des fichiers statistiques sur les matchs de football de différents championnats.

Les fichiers au format CSV ont été récupérés pour les quatre championnats étudiés et les saisons 2020-2021 à 2024-2025.

Les données ont ensuite été organisées par saison et par championnat afin de faciliter leur traitement avec Python.

Le travail de préparation a notamment consisté à :

- Regrouper les fichiers correspondant aux quatre championnats.
- Identifier les saisons et les championnats associés à chaque fichier.
- Harmoniser les données pour obtenir une structure commune.
- Sélectionner les variables nécessaires aux analyses.
- Préparer un jeu de données consolidé destiné à l'analyse exploratoire et à Power BI.
  
Le jeu de données final a été exporté au format CSV afin de faciliter son utilisation dans les étapes suivantes.

## 6. Nettoyage des données et difficultés rencontrées

Une attention particulière a été accordée à la qualité et à la cohérence des données avant leur exploitation.

Plusieurs contrôles ont été réalisés :

- Vérification de la cohérence des championnats et des saisons.
- Contrôle des plages de dates présentes dans les fichiers.
- Recherche de valeurs négatives dans les variables numériques.
- Vérification des types de données.
- Contrôle de la cohérence des informations entre les différents fichiers.
- Préparation du jeu de données final pour son exploitation dans Power BI.

Les anomalies, les difficultés rencontrées, les corrections apportées et les résultats des contrôles sont détaillés dans la documentation technique :

[Consulter la documentation sur le nettoyage et l'analyse exploratoire](docs/data_cleaning_and_eda.md).

## 7. Analyse exploratoire et résultats

L'analyse exploratoire (EDA) a permis d'étudier les performances des équipes, les différences entre les championnats et les tendances observées au cours des saisons.

### 7.1. Vue globale du dataset

Le jeu de données consolidé présente les caractéristiques suivantes :

| Indicateur | Résultat |
|---|---:|
| Nombre total de matchs | 7 082 |
| Nombre total de buts | 20 116 |
| Moyenne de buts par match | 2,84 |

### 7.2. Comparaison des championnats

Les statistiques globales par championnat mettent en évidence certaines différences de performances.

| Championnat | Matchs | Buts | Moyenne de buts / match |
|---|---:|---:|---:|
| Bundesliga | 1 530 | 4 797 | 3,14 |
| Premier League | 1 900 | 5 540 | 2,92 |
| Ligue 1 | 1 752 | 4 920 | 2,81 |
| La Liga | 1 900 | 4 859 | 2,56 |

La Bundesliga présente la moyenne de buts par match la plus élevée parmi les quatre championnats étudiés, tandis que La Liga affiche la moyenne la plus faible.

### 7.3. Performances à domicile et à l'extérieur

La comparaison des performances à domicile et à l'extérieur révèle un avantage statistique pour les équipes qui jouent à domicile.

| Indicateur | Domicile | Extérieur |
|---|---:|---:|
| Moyenne de buts | 1,55 | 1,29 |
| Moyenne de tirs | 13,57 | 11,23 |
| Moyenne de tirs cadrés | 4,83 | 4,00 |
| Moyenne de corners | 5,32 | 4,38 |

Les équipes à domicile affichent des moyennes supérieures pour l'ensemble des indicateurs présentés.

### 7.4. Classement des équipes par nombre de buts

L'analyse des buts inscrits par équipe fait ressortir les quatre équipes suivantes :

| Équipe | Nombre de buts |
|---|---:|
| Bayern Munich | 481 |
| Manchester City | 444 |
| Paris Saint-Germain | 438 |
| Liverpool | 409 |

### 7.5. Principaux enseignements

Les analyses réalisées permettent de dégager plusieurs observations :

- La Bundesliga est le championnat avec la moyenne de buts par match la plus élevée (3,14).
- Les équipes à domicile présentent des moyennes supérieures en matière de buts, de tirs, de tirs cadrés et de corners.
- Le Bayern Munich arrive en tête des équipes étudiées en nombre de buts inscrits, avec 481 réalisations.
- Les différences entre les championnats montrent l'intérêt d'une analyse comparative sur plusieurs saisons.
## 8. Modélisation et mesures DAX

Après la préparation des données avec Python, le jeu de données nettoyé a été importé dans Power BI.

Cette étape a consisté à :

- Organiser le modèle de données.
- Créer une table de référence pour les championnats.
- Mettre en place les relations entre les tables.
- Développer des mesures DAX pour calculer les principaux indicateurs de performance.

Parmi les indicateurs développés :

- Nombre total de matchs.
- Nombre total de buts.
- Moyenne de buts par match.
- Nombre de victoires à domicile.
- Pourcentage de victoires à domicile.

Ces mesures permettent d'alimenter les visualisations et de suivre les performances selon les filtres sélectionnés.

## 9. Dashboard Power BI

Le projet comprend un tableau de bord interactif développé avec Power BI.

Il permet notamment de consulter les principaux indicateurs et de filtrer les résultats selon les championnats étudiés.

Une version PDF du tableau de bord est disponible pour consulter les visualisations et les principaux indicateurs du projet.
[Consulter le dashboard Power BI (PDF)](images/dashboard_preview.pdf)

## 10. Structure du projet

La structure du dépôt GitHub est organisée autour des différentes étapes du projet :

```text
football-analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── dashboard/
│
├── docs/
│   └── data_cleaning_and_eda.md
│
├── README.md
└── requirements.txt
```

## 11. Conclusion et compétences développées

Ce projet m'a permis de mettre en pratique différentes compétences liées à l'analyse de données et à la Business Intelligence.

Il m'a notamment permis de travailler sur :

- La manipulation et le nettoyage de données avec Python et Pandas.
- La réalisation d'analyses exploratoires.
- La recherche d'anomalies et le contrôle de la qualité des données.
- L'interprétation de résultats statistiques.
- La modélisation de données dans Power BI.
- La création de mesures avec DAX.
- La conception de tableaux de bord interactifs.

Ce travail constitue une mise en application concrète de compétences en **Data Analytics et Business Intelligence**, depuis les données brutes jusqu'à leur visualisation.
