import streamlit as st

def initial_choice(max_value):
    '''
    Página inicial do quiz, mostra quais cápitulos se pode fazer o quiz
    é necessario passar o 'max_value' para podermos identificar quantas questões
    temos no banco de questão
    '''
    st.subheader('Escolha como deseja fazer o questionário!',text_alignment='center')

    # Lista de Cápitulos escolhido pelo o usuário
    escolhas_cap = st.pills(label='Qual cápitulo deseja simular a prova', 
                            options=['Capítulo 1', 'Capítulo 2', 'Capítulo 3'], 
                            selection_mode='multi')
    
    # Número de questão simuladas pelo o usuário
    num_questoes = st.number_input(label=f'Escolha o número de questões para simular. Max({max_value})', 
                                   min_value=5,
                                   max_value=max_value,
                                   value=20, 
                                   step=int()
                                    )
    
    # Botão iniciar só é ativado quando o usuário escolher pelo menos 1 capítulo a ser simulado
    iniciar = st.button('iniciar', 
                        disabled=(len(escolhas_cap) == 0)
                        )
    if iniciar:
        return escolhas_cap, num_questoes
