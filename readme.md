# ReadmoreAi

Bem-vindo ao repositório do projeto **ReadmoreAi**! Este projeto tem como objetivo gerar sugestões personalizadas de livros com base nas preferências do usuário, utilizando técnicas de processamento de linguagem natural e análise de dados. Abaixo, você encontrará os passos necessários para configurar e executar o projeto em sua máquina local.

## Pré-requisitos

Antes de começar, certifique-se de que você possui os seguintes requisitos instalados:

- **Python 3.x**
- **pip** (gerenciador de pacotes do Python)

## Passos para Configuração e Execução

### 1. Criar um Ambiente Virtual (venv)

Primeiro, crie um ambiente virtual para isolar as dependências do projeto. Execute o seguinte comando no terminal:

```bash
python -m venv env
```

Isso criará uma pasta chamada `env` que conterá o ambiente virtual.

### 2. Ativar o Ambiente Virtual

Após criar o ambiente virtual, ative-o:

**No Windows:**

```bash
.\env\Scripts\activate
```

**No macOS/Linux:**

```bash
source env/bin/activate
```

### 3. Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências do projeto usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados

Antes de executar o projeto, é necessário configurar o banco de dados. Execute o seguinte comando para criar as tabelas e estruturas necessárias:

```bash
python db/create.py
```

### 5. Executar o Projeto

Agora que tudo está configurado, você pode executar o projeto. Utilize o seguinte comando para iniciar o servidor do **Streamlit**:

```bash
streamlit run main.py
```

Isso abrirá uma nova aba no seu navegador com a interface do projeto.

## Estrutura do Projeto

Aqui está uma visão geral da estrutura do projeto:

```
ReadmoreAi/
│
├── db/
│   ├── books.py          # Gerenciamento de livros no banco de dados
│   ├── create.py         # Script para criar o banco de dados
│   ├── users.py          # Gerenciamento de usuários no banco de dados
│
├── env/                  # Ambiente virtual
│
├── img/                  # Diretório para armazenar imagens
│
├── src/
│   ├── initialize.py     # Inicialização do projeto
│   ├── mybooks.py        # Gerenciamento de livros
│   ├── pages.py          # Configuração das páginas
│   ├── principal.py      # Arquivo principal do projeto
│   ├── suggest.py        # Sistema de sugestões
│
├── main.py               # Ponto de entrada principal do projeto
│
├── requirements.txt      # Lista de dependências do projeto
│
└── readme.md             # Este arquivo
```

## Integrantes do Projeto

Este projeto foi desenvolvido por:

- Adriana Melcop
- Eduarda Albuquerque
- Getulio Junqueira
- Marcela Raposo
- Thawan Silva
