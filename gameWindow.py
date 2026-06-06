import streamlit as st
from getQuestions import get_questions
from initialWindow import initial_choice
from random import sample

st.set_page_config('Quiz Eng. de Software I', page_icon='🕹️') 

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

#===========================================
# Função para processar resposta do usuário
#===========================================
def responder(resposta):
    if st.session_state.respondidos[st.session_state.indice]:
        return
    
    st.session_state.respondeu = True
    st.session_state.respondidos[st.session_state.indice] = True
    
    # Pega a pergunta atual com base no estado para evitar erros de escopo
    pergunta_atual_local = st.session_state.dadosFiltrados[st.session_state.randIndice[st.session_state.indice]]
    resposta_certa = pergunta_atual_local['Resposta'].strip()

    if resposta.lower() == resposta_certa.lower():
        st.session_state.ultimo_toast = ("Acertou! 🎉", "✅")
    else:
        st.session_state.ultimo_toast = ("Errou! 😥", "❌")
        st.session_state.respostas[st.session_state.indice] = False
        st.session_state.erros.append(st.session_state.indice)
    
    # NOTA: Removida a lógica de "gameOver" daqui. Ela foi passada para o botão da última questão.

#=============================================
# Inicialização dos dados do banco de questão
#=============================================
if 'dados' not in st.session_state:
    with st.spinner('Carregando questionário...'):
        st.session_state.dados = get_questions()

    st.session_state.recarregar_dados = False
    st.session_state.config = False 
    st.session_state.gameOver = False

#=======================
# Tela de Configurações
#=======================
if not st.session_state.config:

    # Carrega tela de configurações do quiz
    result = initial_choice(len(st.session_state.dados))
    
    if st.session_state.get("recarregar_dados", False):
        extra_sheets = st.session_state.get('extra_sheets', [])
        st.session_state.dados = get_questions(extra_sheets)
        st.session_state.recarregar_dados = False

    if result is not None:
        capitulos, numQuestoes = result 

        st.session_state.capitulos = capitulos

        st.session_state.dadosFiltrados = [x for x in st.session_state.dados
                                           if any(x['Tópico da questão'].startswith(cap) for cap in capitulos)]
        
        st.session_state.numQuestoes = len(st.session_state.dadosFiltrados) if len(st.session_state.dadosFiltrados) < numQuestoes else numQuestoes
        
        if st.session_state.numQuestoes == 0:
            st.warning("⚠️ Não foi encontrado nenhum resultado para esse capítulo ainda!")
            st.stop()
        
        st.session_state.randIndice = sample(range(0, len(st.session_state.dadosFiltrados)), st.session_state.numQuestoes)

        st.session_state.respondeu = False
        st.session_state.indice = 0
        st.session_state.respondidos = [False for _ in range(st.session_state.numQuestoes)]
        st.session_state.respostas = [True for _ in range(st.session_state.numQuestoes)] 
        st.session_state.erros = []
        st.session_state.config = True
        st.rerun()
    
    st.stop()

#=====================
# Tela de Fim de Quiz
#=====================
if st.session_state.gameOver:
    st.balloons()
    st.title("🏆 Fim de Jogo!")

    total = st.session_state.numQuestoes
    acertos = sum(st.session_state.respostas)

    pontos_porcent = acertos / total if acertos <= total else 0

    st.metric('Pontuação final', f'{acertos}/{total}')

    col1, col2 = st.columns([3,1])

    with col1:
        st.progress(pontos_porcent) 
    with col2:
        st.write(f'Você acertou {pontos_porcent*100:.1f}%')

    if acertos == total:
        st.success("Parabéns! Você gabaritou! 🤓")
    elif acertos > total:
        st.error("Como tu ganhou mais pontos que questões feitas, já ta bagunçando já boy...\n" 
                 "NÃO APERTE O BOTÃO DE RESPOSTA VÁRIAS VEZES DA PRÓXIMA VEZ!!!")   
    elif pontos_porcent >= 0.7:
        st.info("Mandou bem!")   
    elif pontos_porcent > 0.5: 
        st.info("Podemos melhorar, eu confio!")
    else:
        st.warning("Precisa estudar mais um pouco...")
        
    if st.button("Reiniciar Quiz"):
        reiniciar_jogo()

    if len(st.session_state.erros):
        st.markdown("# Questões erradas: \n---\n")
        for i in st.session_state.erros:
            pergunta_errada = st.session_state.dadosFiltrados[st.session_state.randIndice[i]]
            with st.container():
                st.markdown(f"""
## Questão: 
{pergunta_errada['Questão'].strip()}
            
### Resposta: {pergunta_errada['Resposta']}
            
#### Referência:
{pergunta_errada['Citações e referências'].strip()}

---
""")

    st.stop()

#=====================
#  Interface do quiz
#=====================
indice_atual = st.session_state.indice 
pergunta_atual = st.session_state.dadosFiltrados[st.session_state.randIndice[indice_atual]] 

progresso = (st.session_state.indice) / st.session_state.numQuestoes
st.progress(progresso, text=f'Questão {st.session_state.indice + 1} de {st.session_state.numQuestoes}')

head1, head2 = st.columns([4,1])

with head1:
    st.subheader(f"Tópico: {pergunta_atual['Tópico da questão']}")

with head2:
    if st.button('Reiniciar'):
        reiniciar_jogo()

with st.container(border=True): 
    # ERRO DE SINTAXE CORRIGIDO AQUI (aspas duplas por fora)
    st.markdown(f"### {pergunta_atual['Questão']}")

st.write('Essa afirmação é:')

col1, col2 = st.columns(2) 
ant, prox = st.columns(2) 

ja_respondeu = st.session_state.respondeu or st.session_state.respondidos[st.session_state.indice]

with col1: 
    st.button('VERDADEIRA ✅', 
                use_container_width=True, 
                disabled=ja_respondeu,
                on_click=responder,
                args=('verdadeira',)
            )

with col2: 
    st.button('FALSA ❌', 
                use_container_width=True, 
                disabled=ja_respondeu,
                on_click=responder,
                args=('falsa',)
                )

if 'ultimo_toast' in st.session_state and st.session_state.ultimo_toast:
    msg, icon = st.session_state.ultimo_toast
    st.toast(msg, icon=icon)
    st.session_state.ultimo_toast = None

with ant: 
    if st.button("Anterior", use_container_width=True, disabled=(st.session_state.indice == 0)):
        st.session_state.indice -= 1
        st.session_state.respondeu = False # Resetar flag visual
        st.rerun()

with prox: 
    # LÓGICA CORRIGIDA: Se for a última questão, exibe botão para finalizar
    if st.session_state.indice == st.session_state.numQuestoes - 1:
        if st.button("Finalizar Quiz", use_container_width=True, disabled=(not st.session_state.respondidos[st.session_state.indice])):
            st.session_state.gameOver = True
            st.rerun()
    else:
        if st.button("Próximo", use_container_width=True, disabled=(not st.session_state.respondidos[st.session_state.indice])):
            st.session_state.indice += 1
            st.session_state.respondeu = False # Resetar flag visual para a próxima
            st.rerun()

if st.session_state.respondidos[st.session_state.indice]:
    if st.session_state.respostas[st.session_state.indice]:
        st.success(f"""
# ✅ Você ACERTOU a questão! Parabéns 🤩
---
## Questão
{pergunta_atual['Questão'].strip()}

### Resposta
{pergunta_atual['Resposta']}

#### Referência
{pergunta_atual['Citações e referências'].strip()}
""")
    else:
        st.error(f"""
# ❌ Você ERROU a questão! Você consegue na próxima 😥
---
## Questão
{pergunta_atual['Questão'].strip()}

### Resposta
{pergunta_atual['Resposta']}

#### Referência
{pergunta_atual['Citações e referências'].strip()}
""")