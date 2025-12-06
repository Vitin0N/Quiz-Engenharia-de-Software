import streamlit as st
import time
from getQuestions import get_questions
from initialWindow import initial_choice
from random import sample

def reiniciar_jogo():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.session_state.config = False
    st.session_state.gameOver = False
    st.session_state.capitulos = []
    st.session_state.numQuestoes = 0

    st.rerun()


if 'dados' not in st.session_state:
    with st.spinner('Carregando questionario.'):
        st.session_state.dados = get_questions()

    st.session_state.config = False
    st.session_state.gameOver = False


if not st.session_state.config:

    result = initial_choice(len(st.session_state.dados))

    if result is not None:
        capitulos, numQuestoes = result

        st.session_state.capitulos = capitulos

        st.session_state.dadosFiltrados = [x for x in st.session_state.dados
                                           if any(x['Tópico da questão'].startswith(cap) for cap in capitulos)]
        
        st.session_state.numQuestoes = len(st.session_state.dadosFiltrados) if len(st.session_state.dadosFiltrados) < numQuestoes else numQuestoes
        
        st.session_state.randIndice = sample(range(0, len(st.session_state.dadosFiltrados)), st.session_state.numQuestoes)

        st.session_state.indice = 0
        st.session_state.pontos = 0
        st.session_state.config = True
        st.rerun()
    
    st.stop()

if st.session_state.gameOver:
    st.balloons()
    st.title("🏆 Fim de Jogo!")

    total = st.session_state.numQuestoes
    acertos = st.session_state.pontos

    st.metric('Pontuação final', f'{acertos}/{total}')

    if acertos == total:
        st.success("Parabéns! Você gabaritou! 🤓")
    elif acertos > total / 2:
        st.info("Mandou bem!")
    else:
        st.warning("Precisa estudar mais um pouco...")
        
    if st.button("Jogar Novamente"):
        reiniciar_jogo()
    
    st.stop()


indice_atual = st.session_state.indice
pergunta_atual = st.session_state.dadosFiltrados[st.session_state.randIndice[indice_atual]] 

progresso = (st.session_state.indice) / st.session_state.numQuestoes
st.progress(progresso, text=f'Questão {st.session_state.indice + 1} de {st.session_state.numQuestoes}')

st.subheader(f"Tópico: {pergunta_atual['Tópico da questão']}")

with st.container(border=True):
    st.markdown(f'### {pergunta_atual['Questão']}')

st.write('Essa afirmação é:')

col1, col2 = st.columns(2)

resposta_usuario = None

with col1:
    if st.button('VERDADEIRA ✅', use_container_width=True):
        resposta_usuario = 'Verdadeira'

with col2:
    if st.button('FALSA ❌', use_container_width=True):
        resposta_usuario = 'Falsa'

if resposta_usuario:
    resposta_certa = pergunta_atual['Resposta'].strip()

    if resposta_usuario.lower() == resposta_certa.lower():
        st.toast("Acertou! 🎉", icon="✅")
        st.session_state.pontos += 1
        time.sleep(0.7)
    else:
        st.toast(f"Errou! Era {resposta_certa}.", icon="❌")
        time.sleep(1.5)

    if st.session_state.indice + 1 < st.session_state.numQuestoes:
        st.session_state.indice += 1
        st.rerun()
    else:
        st.session_state.gameOver = True
        st.rerun()