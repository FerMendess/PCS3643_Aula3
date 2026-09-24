![Test status](https://github.com/FerMendess/PCS3643_Aula3/actions/workflows/tests.yml/badge.svg)


# PCS3643 - Aula 3: Sistema de Venda de Ingressos de Cinema (MVC)

## Integrantes do Grupo
- Carol Britto Haddad
- Fernando Mendes Seraco  
- Gabriel Agra de Castro Motta
- Mateus Silva de Araújo

---

## Descrição:
O sistema implementa o backend de gerenciamento de cinema em arquitetura **MVC (Model-View-Controller)** com persistência em banco de dados relacional **SQLite** e API REST construída com **FastAPI**.

Funcionalidades contempladas (as mesmas da aula anterior):
- Cadastro e consulta de **Filmes** (com controle de período de exibição e duração).
- Cadastro de **Salas** (número, capacidade e tipo 2D/3D).
- Cadastro de **Tipos de Ingresso** e valores base.
- Cadastro e agendamento de **Sessões** (com validação de choque de horários e integridade de assentos).
- **Listagem de filmes/sessões** disponíveis por data.
- **Compra de Ingressos** (inteira e meia-entrada) com persistência e garantia de atomicidade de assentos.

---

## Como Rodar:

### 1. Compatibilidade de Versões
- **Python**: versão **3.14** (preferencial) ou superior.

### 2. Clonar Repositório
```bash
git clone <url-do-repositorio>
```

### 3. Criar um Ambiente Virtual
```bash
python -m venv .venv
source .venv/bin/activate
```

### 4. Baixar Dependências
```bash
pip install -r requirements.txt
```

### 5. Execução da API
```bash
python app.py
```

Ou diretamente através do Uvicorn:
```bash
uvicorn app:app --reload --port 8000
```

O servidor poderá ser acessado em: `http://127.0.0.1:8000`.

### 6. Execução da Interface
Crie um novo terminal separado, ative novamente o ambiente virtual e rode:

```bash
cd frontend
```

```bash
npm install vite
```

E finalmente:

```bash
npm run dev
```

---

## Documentação

Com o servidor em execução, acesse a documentação interativa e teste as rotas pelo navegador:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Testes Automatizados

**Via Pytest (na raiz do projeto):**
```bash
python -m pytest
```

**Com relatório de cobertura:**
```bash
python -m pytest --cov=EX3
```

---

## Quality Gate
Para linting, formatting e type checking, usamos:

```bash
ruff check --fix;
ruff format;
zuban check;
```

