import numpy as np
import pandas as pd

from donnees_externes import BUT_EN_FINALE, BUTS_CDM, MEILLEUR_JOUEUR_TOURNOI, SOULIER_OR_TOURNOI

STATS = [
    'club_matchs', 'club_minutes', 'club_buts', 'club_passes_d', 'club_clean_sheets',
    'ldc_matchs', 'ldc_minutes', 'ldc_buts', 'ldc_passes_d',
    'champ_matchs', 'champ_minutes', 'champ_buts', 'champ_passes_d',
]

CLUBS_HORS_GRAND_CHAMPIONNAT = {
    'AEK Athènes', 'Ajax', 'Al-Gharafa', 'Al-Hilal', 'Al-Ittihad', 'Al-Nassr', 'Al-Qadsiah',
    'Benfica', 'Celtic', 'Club América', 'Dynamo Kiev', 'FC Porto', 'FK Anji Makhatchkala',
    'Galatasaray', 'Glasgow Rangers', 'Grasshopper Zurich', 'Inter Miami', 'Olympiakos',
    'PSV Eindhoven', 'Panathinaïkos', 'Rapid Vienne', 'Rosenborg BK', 'SK Dnipro-1', 'Santos',
    'Slavia Prague', 'Sporting CP', 'São Paulo FC', 'Vitesse Arnhem',
    'Zénith Saint-Petersbourg', 'Zénith Saint-Pétersbourg',
}

POSTES = {
    'Attaquant': 'attaquant',
    'Milieu': 'milieu',
    'Défenseur': 'defenseur',
    'Gardien': 'gardien',
}


def construire_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in STATS:
        df[col + '_pct'] = df.groupby('Année')[col].rank(pct=True, method='average')

    for poste, nom in POSTES.items():
        df['poste_' + nom] = (df['Poste'] == poste).astype(int)

    def part_grand_championnat(clubs):
        liste = [c.strip() for c in clubs.split('|')]
        return sum(c not in CLUBS_HORS_GRAND_CHAMPIONNAT for c in liste) / len(liste)

    df['grand_championnat'] = df['Clubs'].apply(part_grand_championnat)

    def marquer(liste):
        resultat = np.zeros(len(df), dtype=int)
        for annee, motif in liste:
            resultat |= ((df['Année'] == annee)
                         & df['Nom'].str.contains(motif, regex=False)).values
        return resultat

    df['meilleur_joueur_tournoi'] = marquer(MEILLEUR_JOUEUR_TOURNOI)
    df['but_en_finale'] = marquer(BUT_EN_FINALE)
    df['soulier_or_tournoi'] = marquer(SOULIER_OR_TOURNOI)

    max_ldc = df.groupby('Année')['ldc_buts'].transform('max')
    df['meilleur_buteur_ldc'] = ((df['ldc_buts'] == max_ldc) & (df['ldc_buts'] >= 6)).astype(int)

    buts_cdm = np.zeros(len(df))
    for annee, motif, buts in BUTS_CDM:
        buts_cdm[((df['Année'] == annee) & df['Nom'].str.contains(motif, regex=False)).values] = buts
    df['buts_cdm'] = buts_cdm

    titres = ['titre_ldc', 'titre_championnat', 'titre_coupe_nationale',
              'titre_cdm', 'titre_continental', 'titre_cwc_supercup']
    df['nb_titres'] = df[titres].sum(axis=1)
    df['aucun_titre'] = (df['nb_titres'] == 0).astype(int)
    nb_nommes_club = df.groupby(['Année', 'Club'])['Nom'].transform('count')
    df['log_nb_club'] = np.log(nb_nommes_club)

    return df


if __name__ == '__main__':
    for nom in ['dataset_dl_1995_2025', 'dataset_dl_2026']:
        df = pd.read_csv(f'data/{nom}.csv', sep=';')
        df_clean = construire_features(df)
        df_clean.to_csv(f'data/{nom}.csv', sep=';', index=False)
        print(f'{nom}.csv généré avec succès : {df_clean.shape[0]} lignes, {df_clean.shape[1]} colonnes')