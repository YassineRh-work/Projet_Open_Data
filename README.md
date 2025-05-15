# Projet_Open_Data

## Description
Ce projet vise à exploiter des données ouvertes mondiales pour visualiser des indicateurs de développement par pays et par année.  
L'objectif principal est de nettoyer les données, filtrer un indicateur spécifique, sélectionner certaines années clés, puis représenter ces données sur une carte interactive.

## Fonctionnalités
- Nettoyage et filtrage des données CSV par indicateur.
- Sélection des années spécifiques : 2000, 2005, 2010, 2015, 2020.
- Visualisation interactive sur une carte du monde avec la bibliothèque Folium.
- Interface avec un menu déroulant pour choisir l'année à afficher.

## Technologies utilisées
- Python (pandas, folium)
- Jupyter Notebook / Scripts Python
- Données CSV issues d'indicateurs de développement mondial

## Instructions d’utilisation
1. Charger le fichier CSV contenant les données.
2. Nettoyer et filtrer selon l'indicateur choisi.
3. Exécuter le script pour générer une carte interactive.
4. Utiliser le menu déroulant sur la carte pour changer d'année.

## Exemple de commande
```bash
python nettoyage.py
python map.py
