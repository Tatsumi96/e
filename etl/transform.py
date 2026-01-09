def transform_data(df_source, df_product, df_branch):
    df_source["noCompte"] = df_source["noCompte"].astype(str).str.replace(" ", "")
    df_source["code_banque"] = df_source["noCompte"].astype(str).str[:5]
    df_source["code_agence"] = df_source["noCompte"].astype(str).str[5:10]
    df_source["code_produit"] = df_source["noCompte"].astype(str).str[10:11]
    df_source["numero_compte"] = df_source["noCompte"].astype(str).str[11:-2]

    df_source = df_source[df_source["AccountStatus"].isin(["Actif", "Active"])]

    df_product.columns = ["code_produit", "nom_produit"]
    df_branch.columns = ["code_agence", "nom_agence"]

    df_product["code_produit"] = df_product["code_produit"].astype(str)
    df_branch["code_agence"] = df_branch["code_agence"].astype(int).apply(lambda x: f"{x:05d}")

    gestionnaires = df_source[["gestionnaire de compte"]].drop_duplicates().reset_index(drop=True)
    gestionnaires["id_gestionnaire"] = gestionnaires.index

    df_source = df_source.merge(gestionnaires, on="gestionnaire de compte", how="left")

    fact_comptes = df_source[
        [
            "Code",
            "noCompte",
            "AvailableBalance",
            "OpeningDate",
            "Report_date_to",
            "code_agence",
            "code_produit",
            "id_gestionnaire",
        ]
    ]

    return fact_comptes, df_product, df_branch, gestionnaires
