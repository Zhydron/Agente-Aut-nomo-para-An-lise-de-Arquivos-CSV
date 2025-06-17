# data_loader.py

import pandas as pd

def load_header(path):
    print(f"Função load_header foi chamada com o caminho: {path}")
    try:
        df_head = pd.read_csv(path)
        print(f"Cabeçalho carregado com {len(df_head)} registros.")
        return df_head
    except FileNotFoundError:
        print(f"Erro: Arquivo de cabeçalho não encontrado em {path}")
        return None # Ou raise uma exceção, dependendo do seu tratamento de erro desejado
    except Exception as e:
        print(f"Erro ao carregar cabeçalho: {e}")
        return None


def load_items(path):
    print(f"Função load_items foi chamada com o caminho: {path}")
    try:
        df_items = pd.read_csv(path)
        print(f"Itens carregados com {len(df_items)} registros.")
        return df_items
    except FileNotFoundError:
        print(f"Erro: Arquivo de itens não encontrado em {path}")
        return None
    except Exception as e:
        print(f"Erro ao carregar itens: {e}")
        return None

def merge_data(df1, df2):
    print("Realizando merge dos DataFrames...")
    if df1 is None or df2 is None:
        print("Erro: Um ou ambos os DataFrames para merge são None.")
        return None

    try:
        
        merged_df = pd.merge(
            df1,
            df2,
            on="CHAVE DE ACESSO",
            how="left" # Pode testar com 'inner' também se 'left' continuar dando problema
        )

        print(f"Merge realizado com sucesso! DataFrame resultante tem {len(merged_df)} registros.")
        return merged_df
    except KeyError as ke:
        print(f"Erro ao realizar o merge: A coluna de merge '{ke}' não foi encontrada em um dos DataFrames.")
        print(f"Colunas disponíveis em df1: {df1.columns.tolist()}")
        print(f"Colunas disponíveis em df2: {df2.columns.tolist()}")
        return None
    except Exception as e: # Mantém o tratamento de erro genérico
        print(f"Erro inesperado ao realizar o merge: {e}")
        return None
