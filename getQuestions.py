import streamlit as st
import re

def initial_choice(max_value):
    '''
    Página inicial do quiz, mostra quais cápitulos se pode fazer o quiz
    é necessario passar o 'max_value' para podermos identificar quantas questões
    temos no banco de questão
    '''

    if 'extra_sheets' not in st.session_state:
        st.session_state.extra_sheets = []
    
    st.subheader('Escolha como deseja fazer o questionário!', anchor=False)

    # 1. Uso de st.form para evitar duplo envio (loop)
    with st.form("form_novo_banco", clear_on_submit=True):
        novo_banco = st.text_input('Adicionar um novo banco de questões (do google sheet)!')
        submit_banco = st.form_submit_button("Adicionar Banco")

        if submit_banco:
            if novo_banco.strip():
                match_id = re.search(r"/d/([a-zA-Z0-9-_]+)", novo_banco)
                match_gid = re.search(r"gid=([0-9]+)", novo_banco)

                if match_id and match_gid:
                    sheet_id = match_id.group(1)
                    sheet_gid = match_gid.group(1)
                    ja_existe = False

                    # verifica nos secrets
                    for id_secret, gid_secret in zip(st.secrets["SHEET_ID"], st.secrets["SHEET_GID"]):
                        if sheet_id == id_secret and str(sheet_gid) == str(gid_secret):
                            ja_existe = True
                            break

                    # verifica nos extras
                    if not ja_existe:
                        ja_existe = any(
                            s["id"] == sheet_id and str(s["gid"]) == str(sheet_gid)
                            for s in st.session_state.extra_sheets
                        )

                    if ja_existe:
                        st.warning("Esse banco já está cadastrado!")
                    else:
                        st.session_state.extra_sheets.append({
                            "id": sheet_id,
                            "gid": sheet_gid
                        })

                        st.session_state.recarregar_dados = True
                        st.success("Banco de questões adicionado!")
                else:
                    st.error("Link inválido! Certifique-se de colar a URL completa.")
            else:
                st.warning("Por favor, insira um link.")

    # Lista de Cápitulos escolhidos pelo usuário
    escolhas_cap = st.pills(label='Qual cápitulo deseja simular a prova', 
                            options=['Capítulo 1', 'Capítulo 2', 'Capítulo 3', 
                                     'Capítulo 5', 'Capítulo 7', 'Testes, capítulo 8', 
                                     'Gerenciamento de Projetos, capítulo 22', 'Sistemas Legados, capítulo 8 '], 
                            selection_mode='multi')
    
    if max_value < 1:
        st.warning("⚠️ O banco de questões está vazio. Adicione questões para continuar.")
        st.stop() # Para a execução aqui para não travar o number_input

    # Ajuste dinâmico dos limites
    limite_minimo = min(5, max_value)
    valor_padrao = min(20, max_value)

    # Número de questões simuladas pelo usuário
    num_questoes = st.number_input(label=f'Escolha o número de questões para simular. Max({max_value})', 
                                   min_value=limite_minimo,
                                   max_value=max_value,
                                   value=valor_padrao, 
                                   step=1
                                   )
    
    # Botão iniciar só é ativado quando o usuário escolher pelo menos 1 capítulo a ser simulado
    iniciar = st.button('iniciar', 
                        disabled=(len(escolhas_cap) == 0)
                        )
    if iniciar:
        return escolhas_cap, num_questoes