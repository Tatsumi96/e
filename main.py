from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_to_sqlite
from etl.aggregate import compute_indicators
import pandas as pd

FILE_PATH = "data/dataset_account.xlsx"
DB_PATH = "database.db"

df_source, df_product, df_branch = extract_data(FILE_PATH)

fact_comptes, dim_produit, dim_agence, dim_gestionnaire = transform_data(
    df_source, df_product, df_branch
)

load_to_sqlite(fact_comptes, dim_produit, dim_agence, dim_gestionnaire, DB_PATH)

df_final = pd.merge(fact_comptes, dim_agence, on="code_agence", how="left")

df_final = pd.merge(df_final, dim_produit, on="code_produit", how="left")

df_final = pd.merge(df_final, dim_gestionnaire, on="id_gestionnaire", how="left")



(

    indicators,

    repartition_comptes,

    solde_agence,

    solde_produit,

    top_gestionnaires,

) = compute_indicators(df_final)

print("Total comptes actifs :", indicators["total_comptes_actifs"])

print("\nRépartition des comptes par agence :")
print(repartition_comptes.head())

print("\nSolde par agence :")
print(solde_agence.head())

print("\nSolde moyen par produit :")
print(solde_produit.head())

print("\nTop gestionnaires :")
print(top_gestionnaires)
