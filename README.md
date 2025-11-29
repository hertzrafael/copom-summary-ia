# 📘 **IA para Análise de Ata do COPOM**

Este repositório contém um robô capaz de produzir resumos e tirar dúvidas sobre o assunto.

## Como rodar o projeto?

### 1. Acessar o ambiente virtual
```bash
python -m venv .venv
```

Windows:
```bash
source .venv/Scripts/activate
```

Linux:
```bash
source .venv/bin/activate
```

### 2. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 3. Rodar o streamlit
Lembre-se de executar o comando abaixo na pasta root (mesmo caminho onde está o requirements.txt) do projeto.
```bash
streamlit run src/main.py
```

### 4. Obter as API keys
Hugging face: <a href='https://huggingface.co/settings/tokens'>Obter</a> <br>
Groq: <a href='https://console.groq.com/keys'>Obter</a>

### 5. Atualizar Ata
Clique no botão vermelho `Atualizar COPOM` para obter a última ata divulgada.
