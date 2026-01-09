import pandas as pd

def compute_indicators(df):
    indicators = {}

    indicators["total_comptes_actifs"] = df["noCompte"].nunique()

    repartition_comptes_par_agence = (
        df.groupby("nom_agence")["noCompte"]
        .nunique()
        .reset_index()
        .sort_values(by="noCompte", ascending=False)
    )

    solde_par_agence = (
        df.groupby("nom_agence")["AvailableBalance"]
        .sum()
        .reset_index()
        .sort_values(by="AvailableBalance", ascending=False)
    )

    solde_moyen_par_produit = (
        df.groupby("nom_produit")["AvailableBalance"]
        .mean()
        .reset_index()
        .sort_values(by="AvailableBalance", ascending=False)
    )

    top_gestionnaires = (
        df.groupby("gestionnaire de compte")["AvailableBalance"]
        .sum()
        .reset_index()
        .sort_values(by="AvailableBalance", ascending=False)
        .head(5)
    )

    return (
        indicators,
        repartition_comptes_par_agence,
        solde_par_agence,
        solde_moyen_par_produit,
        top_gestionnaires,
    )
