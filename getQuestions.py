import pandas as pd
import streamlit as st

def get_questions(extra_sheet=None):
    '''
    Busca os registros das perguntas no banco de questões.
    Retorna uma lista de dicionários (formato padrão JSON).
    '''
    
    # 1. Pega as informações do secrets (usando fallback para lista vazia)
    # Convertendo direto para lista para facilitar a manipulação
    secret_ids = list(st.secrets.get("SHEET_ID", []))
    secret_gids = list(st.secrets.get("SHEET_GID", []))

    # 2. Une os IDs e GIDs em pares (Tuplas) para que não se misturem
    planilhas = list(zip(secret_ids, secret_gids))

    # 3. Adiciona as planilhas extras enviadas pelo usuário
    if extra_sheet:
        for sheet in extra_sheet:
            planilhas.append((sheet['id'], sheet['gid']))

    # 4. Remove duplicatas garantindo que o par (id, gid) continue junto
    planilhas_unicas = list(set(planilhas))

    all_questions = []

    # 5. Baixa os dados de cada planilha
    for sheet_id, sheet_gid in planilhas_unicas:
        # Monta a URL de exportação em CSV do Google Sheets
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={sheet_gid}"
        
        try:
            # Lê o CSV usando pandas
            df = pd.read_csv(url)
            
            # (OPCIONAL) Retire as questões testes de Alan. 
            # ATENÇÃO: Substitua 'Nome da Coluna' pelo nome exato da coluna onde está o nome do autor/tipo
            # df = df[df['Nome da Coluna'] != 'Alan']
            
            # Converte o DataFrame para uma lista de dicionários e adiciona à lista final
            all_questions.extend(df.to_dict('records'))
            
        except Exception as e:
            # Mostra um erro na tela em vez de quebrar o site inteiro caso o link seja inválido
            st.error(f"Erro ao carregar a planilha ID {sheet_id}. Verifique se o link é público. Erro: {e}")

    return all_questions