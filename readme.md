# ReadmoreAi

Bem-vindo ao repositório do projeto **ReadmoreAi**! Este projeto tem como objetivo gerar sugestões personalizadas de livros com base nas preferências do usuário, utilizando técnicas de processamento de linguagem natural e análise de dados. Abaixo, você encontrará os passos necessários para configurar e executar o projeto em sua máquina local.

## Tecnologias Utilizadas:
Python e Streamlit

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
python database/create.py
```

### 5. Configurar Chave API

Por último, é necessário adicionar sua chave de API nos arquivos `mybooks.py` e `suggest.py`, dentro da pasta `src`.

Em cada um desses arquivos, encontre a seguinte linha:

```python
genai.configure(api_key='-')
```

Substitua `'-'` pela sua chave de API válida.

### 6. Executar o Projeto

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

## Como utilizar o Projeto

Após seguir os passos de configuração e execução descritos acima, você pode interagir com o **ReadmoreAi** diretamente pela interface web gerada pelo **Streamlit**.


### Funcionalidades Principais:
1. **Cadastro de Usuários:** Ao acessar a interface, você será solicitado a criar uma conta. Isso permite que o sistema personalize as recomendações de livros de acordo com as suas preferências.
   
2. **Recomendações Personalizadas:** O sistema sugere livros com base nas preferências do usuário e no histórico de interações. As sugestões são atualizadas conforme o usuário interage com o sistema.
   
3. **Visualização de Livros:** Você pode ver uma lista de livros recomendados, com detalhes como título, autor e sinopse.

4. **Busca por Livros:** A interface também oferece uma funcionalidade de busca, onde o usuário pode pesquisar por livros específicos.

5. **Atualização do Banco de Dados:** A cada interação com a plataforma, o banco de dados é atualizado com informações sobre os livros mais acessados e as preferências dos usuários.


## Imagens do Projeto

A pasta **img/** contém imagens relacionadas ao projeto.


## Status do Projeto

Atualmente, o projeto está 95% concluído. A única tarefa pendente é a organização dos códigos nos arquivos Python. Isso inclui melhorias no código para facilitar a manutenção e melhorar a legibilidade.

## Diretrizes de Contribuição

Agradecemos pelo seu interesse em contribuir para o projeto **ReadmoreAi**! No entanto, como este é um trabalho acadêmico, **não aceitamos contribuições diretas**. Pedimos que, caso tenha sugestões ou queira colaborar de alguma forma, entre em contato com os responsáveis pelo projeto para discutir possíveis formas de colaboração dentro das diretrizes acadêmicas.

## Integrantes do Projeto

Este projeto foi desenvolvido por:

- Adriana Melcop | atmc@cin.ufpe.br
- Eduarda Albuquerque | evas@cin.ufpe.br
- Getulio Junqueira | gjql@cin.ufpe.br
- Marcela Raposo | mpr@cin.ufpe.br
- Thawan Silva | trs3@cin.ufpe.br
