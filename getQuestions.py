import pandas as pd
import streamlit as st

def get_questions():
    '''
    Busca os registros das perguntas no banco de questões retirando as questões testes de Alan
    retorna uma lista de dicionários (formato padrão JSON) 
    '''
    sheet_ids = st.secrets["SHEET_ID"]
    sheet_gids = st.secrets["SHEET_GID"]

    all_questions = []

    for sheet_id, sheet_gid in zip(sheet_ids, sheet_gids):
        url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={sheet_gid}'
        try:
            # Ler os dados atualizados do banco de questão
            df = pd.read_csv(url)
            
            # Retira os registros de Alan
            df = df.iloc[2:]
            
            # Transforma em dicionario
            all_questions.extend(df.to_dict(orient='records')) 

        except Exception as e:
            print(f'Error: Erro ao buscar as perguntas {e}')
            return []
        
    return all_questions


