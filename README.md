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
   
