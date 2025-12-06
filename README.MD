## 🧠 Quiz Interativo Streamlit

Um aplicativo web simples e divertido, construído com **Streamlit**, para simular um questionário de múltipla escolha (Verdadeiro ou Falso), ideal para estudos e autoavaliação. As questões são dinamicamente carregadas de uma planilha do Google Sheets.

-----

## ✨ Funcionalidades

  * **Configuração Personalizada:** O usuário pode escolher quais capítulos deseja incluir no quiz e definir o número de questões.
  * **Busca Dinâmica de Questões:** As perguntas são importadas em tempo real de uma planilha do Google Sheets, garantindo fácil atualização do conteúdo.
  * **Interface Intuitiva:** Desenvolvido com Streamlit, oferece uma experiência de usuário limpa e interativa.
  * **Feedback Imediato:** O usuário recebe um *toast* de confirmação/erro após cada resposta.
  * **Pontuação e Progresso:** Exibe o progresso em relação ao número total de questões e a pontuação final com uma métrica clara.

-----

## 🛠️ Tecnologias Utilizadas

  * **Python**
  * **Streamlit:** Para a criação da interface web.
  * **Pandas:** Para a leitura e manipulação dos dados da planilha.

-----

## 🚀 Como Executar Localmente

### Pré-requisitos

Certifique-se de ter o **Python** instalado em sua máquina.

### 1\. Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <nome-do-repositorio>
```

### 2\. Criar e Ativar o Ambiente Virtual (Opcional, mas Recomendado)

```bash
python -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate   # No Windows
```

### 3\. Instalar as Dependências

As dependências principais são `streamlit` e `pandas`.

```bash
pip install streamlit pandas
```

### 4\. Executar o Aplicativo

Execute o arquivo principal (presumivelmente `app.py`) usando o Streamlit:

```bash
streamlit run gameWindow.py
```

O aplicativo será aberto automaticamente no seu navegador padrão (geralmente em `http://localhost:8501`).

-----

## 📂 Estrutura dos Arquivos (Baseado nos seus códigos)

O projeto parece ser composto por:

  * **`gameWindow.py` (ou `main.py`):** O arquivo principal que gerencia o fluxo do jogo, o estado da sessão (configuração, pontuação, *game over*) e a exibição das questões.
  * **`initialWindow.py`:** Contém a função `initial_choice` que é responsável pela tela de configuração inicial (seleção de capítulos e número de questões).
  * **`getQuestions.py`:** Contém a função `get_questions` que faz a leitura dos dados do questionário a partir do Google Sheets usando Pandas.

-----

## 🔗 Fonte dos Dados

As questões são carregadas diretamente de uma planilha do Google Sheets, usando um link de exportação CSV.

**ID da Planilha no código (`getQuestions.py`):** `1oreiAVDcHUE2ZlNI2wRquKoSsFjP_TL40cdIH8E3XHs`

Isso permite que o conteúdo do quiz seja atualizado externamente sem a necessidade de modificar o código.

-----

## 🤝 Contribuições

Sinta-se à vontade para sugerir melhorias, reportar *bugs* ou adicionar novas funcionalidades.