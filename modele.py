import numpy as np
from scipy.optimize import minimize

# Définition des différentes ères historiques du vote
ERES_HISTORIQUES = [
    (1995, 2006),
    (2007, 2015),
    (2016, 2021),
    (2022, 2100)
]


def identifier_ere(annee):
    """Retourne l'indice correspondant à l'ère de l'année donnée."""
    return next(i for i, (debut, fin) in enumerate(ERES_HISTORIQUES) if debut <= annee <= fin)


class LogitConditionnelEres:
    """
    Modèle de logit conditionnel avec des coefficients propres à chaque ère :
        poids(ère) = poids_communs + écart(ère)
    """

    def __init__(self, l2=3.0, l2_ecart=30.0, bornes=None):
        self.l2 = l2
        self.l2_ecart = l2_ecart
        self.bornes = bornes

    def fit(self, X, parts, groupes, annees=None):
        annees = groupes if annees is None else annees
        
        # Standardisation des features sur l'ensemble d'entraînement
        self.moyenne = X.mean(axis=0)
        self.ecart_type = X.std(axis=0) + 1e-9
        Z = (X - self.moyenne) / self.ecart_type
        
        nombre_features, nombre_eres = Z.shape[1], len(ERES_HISTORIQUES)

        editions = []
        for g in np.unique(groupes):
            idx = np.where(groupes == g)[0]
            editions.append((idx, identifier_ere(annees[idx[0]]), parts[idx] / parts[idx].sum()))

        def fonction_perte_et_gradient(v):
            w = v[:nombre_features]
            ecarts = v[nombre_features:].reshape(nombre_eres, nombre_features)
            
            perte = 0.0
            grad_w = np.zeros_like(w)
            grad_ecarts = np.zeros_like(ecarts)

            for idx, ere_idx, cible in editions:
                scores = Z[idx] @ (w + ecarts[ere_idx])
                scores -= scores.max()  # Stabilité numérique
                predites = np.exp(scores) / np.exp(scores).sum()
                
                perte -= (cible * np.log(predites + 1e-12)).sum()
                grad_element = -Z[idx].T @ (cible - predites)
                
                grad_w += grad_element
                grad_ecarts[ere_idx] += grad_element

            perte += self.l2 * (w @ w) + self.l2_ecart * (ecarts ** 2).sum()
            grad_w += 2 * self.l2 * w
            grad_ecarts += 2 * self.l2_ecart * ecarts

            grad_total = np.concatenate([grad_w, grad_ecarts.flatten()])
            return perte, grad_total

        bornes_optimisation = None
        if self.bornes is not None:
            bornes_optimisation = list(self.bornes) + [(None, None)] * (nombre_eres * nombre_features)

        resultat_optimisation = minimize(
            fonction_perte_et_gradient,
            np.zeros(nombre_features * (nombre_eres + 1)),
            jac=True,
            method='L-BFGS-B',
            bounds=bornes_optimisation
        )

        v_opt = resultat_optimisation.x
        self.poids_communs = v_opt[:nombre_features]
        self.ecarts = v_opt[nombre_features:].reshape(nombre_eres, nombre_features)
        return self

    def score(self, X, annee):
        Z = (X - self.moyenne) / self.ecart_type
        return Z @ (self.poids_communs + self.ecarts[identifier_ere(annee)])


def bornes_de_signe(features):
    """Définit dynamiquement les contraintes de signe pour chaque feature"""
    features_negatives = {'best_past_rank', 'aucun_titre'}
    
    bornes = []
    for f in features:
        if (f.endswith('_pct') or 
            f.startswith(('titre_', 'finaliste_')) or 
            f in {'podium_cdm', 'distinction_meilleur_buteur', 'past_nominations', 
                  'past_wins', 'past_podiums', 'prev_year_share', 'nb_titres', 
                  'log_nb_club', 'soulier_or_tournoi', 'meilleur_buteur_ldc'}):
            bornes.append((0, None)) 
        elif f in features_negatives:
            bornes.append((None, 0))  
        else:
            bornes.append((None, None))
    return bornes

