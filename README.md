# Prédiction du Ballon d'Or par Modélisation Statistique

Ce projet implémente un modèle de logit conditionnel avec pondération par ère et contraintes de signe pour prédire les classements et vainqueurs du Ballon d'Or (historique et édition 2026).

## Architecture du projet
- `donnees_externes.py` : Répertorie les distinctions et événements clés hors dataset.
- `features.py` : Construit les variables (percentiles, postes, championnats, titres).
- `modele.py` : Contient le modèle d'entraînement (Logit conditionnel par ère).
- `prediction.py` : Exécute la calibration par température, le bootstrap

## Résultat 
| Rang | Joueur | Club |
| :---: | :--- | :--- |
| **1** | Lamine Yamal | FC Barcelone |
| **2** | Lionel Messi | Inter Miami |
| **3** | Kylian Mbappé | Real Madrid |
| **4** | Lautaro Martínez | Inter Milan |
| **5** | Vitinha | Paris Saint-Germain |
| **6** | Harry Kane | Bayern Munich |
| **7** | Ousmane Dembélé | Paris Saint-Germain |
| **8** | Fabián Ruiz | Paris Saint-Germain |
| **9** | Khvicha Kvaratskhelia | Paris Saint-Germain |
| **10** | Erling Haaland | Manchester City |
   
## Tutoriel d'utilisation

### 1. Prérequis
Assurez-vous d'avoir **Python 3.8+** installé sur votre machine.

### 2. Installation
Téléchargez le projet et installez les dépendances nécessaires à l'aide du fichier `requirements.txt` :
```bash
pip install -r requirements.txt
```

### 3. Structure des dossiers
Le projet repose sur l'organisation suivante :
- `data/` : Contient les jeux de données historiques (`dataset_dl_1995_2025.csv`) et l'année cible (`dataset_dl_2026.csv`).
- `donnees_externes.py` : Événements extérieurs (buts en finale, meilleurs joueurs de tournoi, etc.).
- `features.py` : Script de traitement et de calcul des variables statistiques.
- `modele.py` : Implémentation de l'algorithme de logit conditionnel par ère.
- `prediction.py` : Script principal orchestrant l'entraînement, la calibration et l'export.

### 4. Lancer la prédiction
Exécutez le script depuis la racine du projet :
```bash
python prediction.py
```

Le script va charger l'historique, calibrer la température, effectuer une simulation par bootstrap pour estimer la robustesse, afficher le top 10 dans la console.
