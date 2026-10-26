from datetime import datetime
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
import importlib

modeles = importlib.import_module('modele')

CIBLE = 'Part des points'

PREMIERE_ANNEE_TEST = 2005
ANNEE_CIBLE = 2026

NOMBRE_BOOTSTRAP = 100

# Groupes de caractéristiques du modèle
STATS_POURCENTAGES = [
    'club_matchs_pct', 'club_minutes_pct', 'club_buts_pct', 'club_passes_d_pct',
    'club_clean_sheets_pct', 'ldc_matchs_pct', 'ldc_minutes_pct', 'ldc_buts_pct',
    'ldc_passes_d_pct', 'champ_matchs_pct', 'champ_minutes_pct', 'champ_buts_pct',
    'champ_passes_d_pct',
]
POSTES = ['poste_attaquant', 'poste_milieu', 'poste_defenseur', 'poste_gardien']
TITRES = [
    'titre_ldc', 'finaliste_ldc', 'titre_championnat', 'titre_coupe_nationale',
    'titre_cdm', 'finaliste_cdm', 'podium_cdm', 'titre_continental',
    'finaliste_continental', 'titre_cwc_supercup', 'distinction_meilleur_buteur',
]
HISTORIQUE_JOUEUR = ['past_nominations', 'past_wins', 'past_podiums', 'prev_year_share', 'best_past_rank']
AUTRES = ['Age', 'grand_championnat']
RESIDUS = ['aucun_titre', 'log_nb_club', 'nb_titres']

FEATURES_OFFICIELLES = STATS_POURCENTAGES + POSTES + TITRES + HISTORIQUE_JOUEUR + AUTRES + RESIDUS
FEATURES_COMPLETES = FEATURES_OFFICIELLES + ['soulier_or_tournoi', 'meilleur_buteur_ldc']


def charger_donnees():
    """Charge les données historiques et les candidats de l'année cible."""
    historique = pd.read_csv('data/dataset_dl_1995_2025.csv', sep=';')
    candidats_2026 = pd.read_csv('data/dataset_dl_2026.csv', sep=';')
    return historique, candidats_2026


def definir_bornes(features):
    """Applique des contraintes de signe, notamment pour les nouvelles distinctions."""
    features_positives_extra = {'soulier_or_tournoi', 'meilleur_buteur_ldc'}
    bornes_modele = modeles.bornes_de_signe(features)
    return [(0, None) if feature in features_positives_extra else b
            for feature, b in zip(features, bornes_modele)]


def entrainer_modele(donnees_entrainement, features, groupe_colonne='Année'):
    """Entraîne"""
    modele = modeles.LogitConditionnelEres(bornes=definir_bornes(features))
    return modele.fit(
        donnees_entrainement[features].values.astype(float),
        donnees_entrainement[CIBLE].values,
        donnees_entrainement[groupe_colonne].values,
        donnees_entrainement['Année'].values
    )


def appliquer_softmax(scores, temperature=1.0):
    scores_ajustes = (scores - scores.max()) / temperature
    exponentielles = np.exp(scores_ajustes)
    return exponentielles / exponentielles.sum()


def calibrer_temperature(historique, features):
    resultats_historiques = []
    
    for annee in sorted(historique['Année'].unique()):
        if annee < PREMIERE_ANNEE_TEST:
            continue
        train = historique[historique['Année'] < annee]
        test = historique[historique['Année'] == annee].reset_index(drop=True)
        
        scores = entrainer_modele(train, features).score(test[features].values.astype(float), annee)
        indice_vrai_gagnant = int(np.where(test['Rang'] == 1)[0][0])
        resultats_historiques.append((scores, indice_vrai_gagnant))

    def fonction_perte(temperature):
        perte_totale = 0
        for scores, gagnant in resultats_historiques:
            probabilites = appliquer_softmax(scores, temperature)
            perte_totale -= np.log(probabilites[gagnant] + 1e-12)
        return perte_totale

    optimisation = minimize_scalar(fonction_perte, bounds=(0.05, 3.0), method='bounded')
    return optimisation.x


def simuler_bootstrap(historique, candidats_2026, features, nombre_iterations=NOMBRE_BOOTSTRAP, graine=42):
    generateur_aleatoire = np.random.default_rng(graine)
    annees_disponibles = historique['Année'].unique()
    features_2026 = candidats_2026[features].values.astype(float)
    compteur_victoires = pd.Series(0.0, index=candidats_2026['Nom'])

    for _ in range(nombre_iterations):
        # Tirage aléatoire des années avec remise pour former un faux historique
        annees_tirees = generateur_aleatoire.choice(annees_disponibles, len(annees_disponibles), replace=True)
        train = pd.concat([
            historique[historique['Année'] == annee].assign(groupe=index_groupe)
            for index_groupe, annee in enumerate(annees_tirees)
        ])
        
        scores = entrainer_modele(train, features, groupe_colonne='groupe').score(features_2026, ANNEE_CIBLE)
        vainqueur_simulation = candidats_2026['Nom'].iloc[np.argmax(scores)]
        compteur_victoires[vainqueur_simulation] += 1

    return 100 * compteur_victoires / nombre_iterations


def predire_classement(historique, candidats_2026, features, nom_version):
    """Exécute la calibration, la prédiction finale et le bootstrap, puis affiche le classement"""
    temperature_optimale = calibrer_temperature(historique, features)
    scores_bruts = entrainer_modele(historique, features).score(candidats_2026[features].values.astype(float), ANNEE_CIBLE)
    
    score_tri = 100 * appliquer_softmax(scores_bruts, temperature_optimale)
    
    resultat = pd.DataFrame({
        'Nom': candidats_2026['Nom'].values,
        '_score_interne': score_tri,
    })
    
    if 'Club' in candidats_2026.columns:
        resultat['Club'] = candidats_2026['Club'].values
        
    resultat = resultat.sort_values('_score_interne', ascending=False).reset_index(drop=True)
    resultat.insert(0, 'rang', range(1, len(resultat) + 1))
    
    resultat = resultat.drop(columns=['_score_interne'])
    
    print(f'\n=== CLASSEMENT ===')
    print(resultat.head(10).to_string(index=False))
    return resultat


if __name__ == '__main__':
    historique, candidats_2026 = charger_donnees()
    classement_final = predire_classement(historique, candidats_2026, FEATURES_COMPLETES, 'OFFICIEL')

