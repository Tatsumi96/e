import pandas as pd

def extract_data(file_path):
    df_source = pd.read_excel(file_path, sheet_name="data source")
    df_product = pd.read_excel(file_path, sheet_name="product mapping")
    df_branch = pd.read_excel(file_path, sheet_name="branch mapping")

    return df_source, df_product, df_branch
