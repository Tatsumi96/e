import sqlite3

def load_to_sqlite(fact_comptes, dim_produit, dim_agence, dim_gestionnaire, db_path="database.db"):
    conn = sqlite3.connect(db_path)

    fact_comptes.to_sql("fact_comptes", conn, if_exists="replace", index=False)
    dim_produit.to_sql("dim_produit", conn, if_exists="replace", index=False)
    dim_agence.to_sql("dim_agence", conn, if_exists="replace", index=False)
    dim_gestionnaire.to_sql("dim_gestionnaire", conn, if_exists="replace", index=False)

    conn.close()
