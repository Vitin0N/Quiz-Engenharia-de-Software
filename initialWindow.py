import streamlit as st

def initial_choice(max_value):
    st.subheader('Escolha como deseja fazer o questionário!',text_alignment='center')

    escolhas_cap = st.pills(label='Qual cápitulo deseja simular a prova', 
                            options=['Capítulo 1', 'Capítulo 2'], 
                            selection_mode='multi')
    
    num_questoes = st.number_input(label=f'Escolha o número de questões para simular. Max({max_value})', 
                                   min_value=5,
                                   max_value=max_value,
                                   value=20, 
                                   step=int()
                                    )
    
    iniciar = st.button('iniciar', 
                        disabled=(len(escolhas_cap) == 0)
                        )
    if iniciar:
        return escolhas_cap, num_questoes
