import pandas as pd
import json

def get_questions():
    '''
    Busca os registros das perguntas no banco de questões retirando as questões testes de Alan
    retorna uma lista de dicionários (formato padrão JSON) 
    '''
    sheet_id = '1oreiAVDcHUE2ZlNI2wRquKoSsFjP_TL40cdIH8E3XHs'
    sheet_gid = '51751594'

    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={sheet_gid}'

    try:
        # Ler os dados atualizados do banco de questão
        df = pd.read_csv(url)
        
        # Retira os registros de Alan
        df = df.iloc[2:]
        
        # Transforma em dicionario
        all_questions = df.to_dict(orient='records')

        return all_questions

    except Exception as e:
        print(f'Error: Erro ao buscar as perguntas {e}')
        return []


