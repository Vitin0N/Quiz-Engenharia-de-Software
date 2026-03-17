import streamlit as st
import time
from getQuestions import get_questions
from initialWindow import initial_choice
from random import sample

st.set_page_config('Quiz Eng. de Software I', page_icon='🕹️') # Setup do cabeçalho da página

def reiniciar_jogo():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.session_state.config = False
    st.session_state.gameOver = False
    st.session_state.capitulos = []
    st.session_state.respondidos = []
    st.session_state.numQuestoes = 0
    st.session_state.erros = []

    st.rerun()

def responder(resposta):
    if st.session_state.respondidos[st.session_state.indice]:
        return
    
    st.session_state.respondeu = True
    st.session_state.respondidos[st.session_state.indice] = True
    resposta_certa = pergunta_atual['Resposta'].strip()

    if resposta.lower() == resposta_certa.lower():
        st.session_state.ultimo_toast = ("Acertou! 🎉", "✅")
        st.session_state.pontos += 1
    else:
        st.session_state.ultimo_toast = ("Errou! 😥", "❌")
        st.session_state.respostas[st.session_state.indice] = False
        st.session_state.erros.append(st.session_state.indice)

    #========================================
    # Definir próxima pergunta ou fim de jogo
    #========================================

    # Caso ainda tenha alguma pergunta para responder o Quiz continua
    if st.session_state.indice + 1 < st.session_state.numQuestoes: # Vai para próxima pergunta
        st.session_state.respondeu = False # Define a próxima pergunta como não respondida

    # Caso não tenha mais questões inicializa a tela de Fim de Jogo
    else: 
        st.session_state.gameOver = True
        st.session_state.respondeu = False



#=============================================
# Inicialização dos dados do banco de questão
#=============================================
if 'dados' not in st.session_state:
    with st.spinner('Carregando questionario.'):
        st.session_state.dados = get_questions()

    st.session_state.config = False 
    st.session_state.gameOver = False

#=======================
# Tela de Configurações
#=======================
if not st.session_state.config:

    # Carrega tela de configurações do quiz
    result = initial_choice(len(st.session_state.dados))

    if result is not None:
        capitulos, numQuestoes = result # Defiene os capítulos selecionados e o num de questões

        st.session_state.capitulos = capitulos

        st.session_state.dadosFiltrados = [x for x in st.session_state.dados
                                           if any(x['Tópico da questão'].startswith(cap) for cap in capitulos)]
        
        # Verifica se tem uma quantidade de questões escolhidas
        # Caso tenha menos do que o escolhido o num de questões fica com o tamanho da lista de questões
        st.session_state.numQuestoes = len(st.session_state.dadosFiltrados) if len(st.session_state.dadosFiltrados) < numQuestoes else numQuestoes
        
        # Randomiza as questões escolhidas
        st.session_state.randIndice = sample(range(0, len(st.session_state.dadosFiltrados)), st.session_state.numQuestoes)

        # Verifica se o usuário responder para disabilitar os botões de resposta (não funciona corretamente)
        st.session_state.respondeu = False

        st.session_state.indice = 0
        st.session_state.respondidos = [False for i in range(st.session_state.numQuestoes)]
        st.session_state.respostas = [True for i in range(st.session_state.numQuestoes)] # repostas corretas ou falsas
        st.session_state.erros = []
        st.session_state.pontos = 0
        st.session_state.config = True
        st.rerun()
    
    st.stop()

#=====================
# Tela de Fim de Quiz
#=====================
if st.session_state.gameOver:
    st.balloons()
    st.title("🏆 Fim de Jogo!")

    # Total de perguntas selecionadas
    total = st.session_state.numQuestoes
    # Numero de acertos (mas só mostra se o numero de acertos não for maior que o total)
    acertos = st.session_state.pontos if st.session_state.pontos <= total else 0

    # Porcentagens de pontos feitos (caso maior que o número de questões é zerado)
    pontos_porcent = acertos / total if acertos <= total else 0

    # Acertos finais
    st.metric('Pontuação final', f'{acertos}/{total}')

    col1, col2 = st.columns([3,1])

    with col1:
        st.progress(pontos_porcent) # Barra de porcentagem de questões acertadas
    with col2:
        st.write(f'Você acertou {pontos_porcent*100:.1f}%')

    if acertos == total:
        st.success("Parabéns! Você gabaritou! 🤓")
    elif acertos > total:
        st.error("Como tu ganhou mais pontos que questões feitas, já ta baguçando já boy...\n" 
                "NÃO APERTE O BOTÃO DE RESPOSTA VÁRIAS VEZES DA PROXIMA VEZ!!!")   
    elif acertos / total >= 0.7:
        st.info("Mandou bem!")   
    elif acertos > total / 2: # Taxa de acertos entre 50% e 69% da prova
        st.info("Podemos melhorar, eu confio!")
    else:
        st.warning("Precisa estudar mais um pouco...")
        
    if st.button("Reiniciar Quiz"):
        reiniciar_jogo()

    if len(st.session_state.erros):
        st.markdown("# Questões erradas: \n"+
                    "---\n")
    for i in st.session_state.erros:
        pergunta_atual = st.session_state.dadosFiltrados[st.session_state.randIndice[i]]
        with st.container():
            st.markdown(f"""
## Questão: 
{pergunta_atual['Questão']}
            
### Resposta: {pergunta_atual['Resposta']}
            
#### Referência:
{pergunta_atual['Citações e referências']}

---
""")

    
    st.stop()

#=====================
#  Inteface do quiz
#=====================

indice_atual = st.session_state.indice # Quantas questões foram respondidas
pergunta_atual = st.session_state.dadosFiltrados[st.session_state.randIndice[indice_atual]] 

progresso = (st.session_state.indice) / st.session_state.numQuestoes
st.progress(progresso, text=f'Questão {st.session_state.indice + 1} de {st.session_state.numQuestoes}')

head1, head2 = st.columns([4,1])

with head1:
    st.subheader(f"Tópico: {pergunta_atual['Tópico da questão']}")

with head2:
    if st.button('Reiniciar'):
        reiniciar_jogo()

with st.container(border=True): # Pergunta atual fica dentro de uma caixinha em destaque
    st.markdown(f'### {pergunta_atual['Questão']}')

st.write('Essa afirmação é:')

col1, col2 = st.columns(2) # Colunas onde fica alocados os botões de resposta

ant, prox = st.columns(2) # Colunas onde ficam o anterior e o proximo

# resposta_usuario = None

ja_respondeu = st.session_state.respondeu or st.session_state.respondidos[st.session_state.indice]

with col1: # Botão de resposta verdadeira
    st.button('VERDADEIRA ✅', 
                use_container_width=True, 
                disabled=ja_respondeu,
                on_click=responder,
                args=('verdadeira',)
            )

with col2: # Botão de resposta verdadeira
    st.button('FALSA ❌', 
                use_container_width=True, 
                disabled=ja_respondeu,
                on_click=responder,
                args=('falsa',)
                )

# Toast de validação da resposta
if 'ultimo_toast' in st.session_state and st.session_state.ultimo_toast:
    msg, icon = st.session_state.ultimo_toast
    st.toast(msg, icon=icon)
    st.session_state.ultimo_toast = None


with ant: # Botão de anterior
    if st.button("Anterior", use_container_width=True, disabled=(st.session_state.indice == 0)):
        st.session_state.indice -= 1
        st.rerun()

with prox: # Botão proximo
    if st.button("Próximo", use_container_width=True, disabled=(st.session_state.respondidos[st.session_state.indice] == False)):
        st.session_state.indice += 1
        st.rerun()

# Mostra a reposta correta caso a pessoa tenha errado
if(not st.session_state.respostas[st.session_state.indice]):
    pergunta_atual = st.session_state.dadosFiltrados[st.session_state.randIndice[st.session_state.indice]]

    with st.container():
                st.markdown(f"""
---
                            
## Questão: 
{pergunta_atual['Questão']}
            
### Resposta: {pergunta_atual['Resposta']}
            
#### Referência:
{pergunta_atual['Citações e referências']}

---
""")

