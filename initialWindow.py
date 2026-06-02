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
    
    st.subheader('Escolha como deseja fazer o questionário!',text_alignment='center')

    novo_banco = st.text_input(
        'Adicionar um novo banco de questões (do google sheet)!'
    )

    if novo_banco.strip():
        sheet_id = re.search(r"/d/([a-zA-Z0-9-_]+)", novo_banco)
        sheet_gid = re.search(r"gid=([0-9]+)", novo_banco)

        ja_existe = False

        # verifica nos secrets
        for id_secret, gid_secret in zip(
            st.secrets["SHEET_ID"],
            st.secrets["SHEET_GID"]
        ):
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
            st.rerun()
    else:
        st.error("Link inválido!")


    # Lista de Cápitulos escolhido pelo o usuário
    escolhas_cap = st.pills(label='Qual cápitulo deseja simular a prova', 
                            options=['Capítulo 1', 'Capítulo 2', 'Capítulo 3', 
                                     'Capítulo 5', 'Capítulo 7', 'Testes, capítulo 8', 
                                     'Gerenciamento de Projetos, capítulo 22', 'Sistemas Legados, capítulo 8 '], 
                            selection_mode='multi')
    
    
    # Número de questão simuladas pelo o usuário
    num_questoes = st.number_input(label=f'Escolha o número de questões para simular. Max({max_value})', 
                                   min_value=5,
                                   max_value=max_value,
                                   value=20, 
                                   step=1
                                    )
    
    # Botão iniciar só é ativado quando o usuário escolher pelo menos 1 capítulo a ser simulado
    iniciar = st.button('iniciar', 
                        disabled=(len(escolhas_cap) == 0)
                        )
    if iniciar:
        return escolhas_cap, num_questoes
