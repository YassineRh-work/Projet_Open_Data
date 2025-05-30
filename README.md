# Projet_Open_Data

## Description
Ce projet vise à exploiter des données ouvertes mondiales pour visualiser des indicateurs de développement par pays et par année.  
L'objectif principal est de nettoyer les données, filtrer un indicateur spécifique, sélectionner certaines années clés, puis représenter ces données sur une carte interactive.

## Indicateurs Utilisés
1. Espérance de vie
2. Niveau d’éducation (%)
3. PIB par habitant (USD)
4. Taux de chômage (%)

## Méthode de Calcul de l'IDH
IDH = (Vie_Normalisée * Éducation_Normalisée * Revenu_Normalisé) ** (1/3)
Règles de normalisation :
Espérance de vie : min = 20, max = 85 ans
Éducation : min = 0 %, max = 100 %
Revenu : transformation logarithmique entre 100 et 75 000

## 1. Préparer les données
Tous les fichiers sont déjà générés et disponibles dans les dossiers /result, les commandes ne sont qu'à titre indicatif
```bash
python scripts/gdp/nettoyage.py
python scripts/literacy_rate/nettoyage.py
python scripts/life_expectancy/clean_data.py
python scripts/unemployement/nettoyage.py
```

## 2. Fusionner les données et calculer l'IDH
```bash
python scripts/final_file_and_visualisation_map_scripts/merging_script_update.py
```
## 3. Générer les cartes interactives
```bash
python scripts/final_file_and_visualisation_map_scripts/map3.py
```
**Chaque carte comprend :**
-**Une couche choroplèthe de l’IDH**
-**Des marqueurs pour chaque pays avec une infobulle affichant :**
-**Espérance de vie**
-**Niveau d’éducation**
-**PIB/habitant**
-**IDH**
-**Chômage**

## Dépendances
```bash
pip install pandas numpy folium requests
```
## Auteurs
-Lokeshwaran Vengadabady
-Yassine Rhourri
-Chouaib Skitou
-Hamoudia Camara




