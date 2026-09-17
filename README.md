# PCS3643 - Aula 3: Sistema de Venda de Ingressos de Cinema (MVC)

## Integrantes do Grupo
- Gabriel Agra de Castro Motta
- Fernando Mendes Seraco  
*(outros faltaram por doença)*

---

## 📋 Descrição do Projeto
Aplicação desenvolvida para a disciplina PCS3643 (Laboratório de Engenharia de Software) da Poli-USP.  
O sistema implementa o backend de gerenciamento de cinema em arquitetura **MVC (Model-View-Controller)** com persistência em banco de dados relacional **SQLite** e API REST construída com **FastAPI**.

Funcionalidades contempladas:
- Cadastro e consulta de **Filmes** (com controle de período de exibição e duração).
- Cadastro de **Salas** (número, capacidade e tipo 2D/3D).
- Cadastro de **Tipos de Ingresso** e valores base.
- Cadastro e agendamento de **Sessões** (com validação de choque de horários e integridade de assentos).
- **Listagem de filmes/sessões** disponíveis por data.
- **Compra de Ingressos** (inteira e meia-entrada) com persistência e garantia de atomicidade de assentos.

---

## ⚙️ Requisitos para Execução

### 1. Sistema Operacional e Interpretador
- **Python**: versão **3.10** ou superior (testado e homologado em Python 3.14).
- Sistema Operacional: Windows, Linux ou macOS.

### 2. Dependências Python
As dependências do projeto estão listadas em `EX3/requirements.txt`:
- `fastapi >= 0.110.0` (Framework web para a API REST)
- `uvicorn >= 0.28.0` (Servidor ASGI para execução do FastAPI)
- `pydantic >= 2.6.0` (Validação de schemas e tipagem)
- `httpx >= 0.27.0` (Cliente HTTP para execução da suíte de testes do FastAPI)
- `pytest >= 8.0.0` (Framework para execução dos testes automatizados)

---

## 🚀 Como Instalar e Rodar a Aplicação

### Passo 1: Clonar o repositório
```bash
git clone <url-do-repositorio>
cd PCS3643_Aula3
```

### Passo 2: Criar e ativar um ambiente virtual (recomendado)

**No Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**No Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Passo 3: Instalar as dependências
```bash
pip install -r EX3/requirements.txt
```

### Passo 4: Executar o servidor da API

Navegue até o diretório `EX3` e execute:

```bash
cd EX3
python app.py
```

Ou execute diretamente através do Uvicorn:
```bash
cd EX3
uvicorn app:app --reload --port 8000
```

O servidor iniciará localmente em: `http://127.0.0.1:8000`.

---

## 📖 Documentação Interativa da API (Swagger / OpenAPI)

Com o servidor em execução, acesse a documentação interativa e teste as rotas diretamente pelo navegador:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Status da API**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧪 Execução dos Testes Automatizados

O projeto conta com uma suíte de 58 testes automatizados cobrindo regras de negócio, persistência SQLite, controladores MVC e endpoints REST.

**Via Pytest (na raiz do projeto):**
```bash
python -m pytest
```

**Com relatório de cobertura:**
```bash
python -m pytest --cov=EX3
```

**Linter e Verificação de Tipos:**
```bash
python -m ruff check EX3
python -m mypy EX3
```

---

## 📁 Estrutura do Diretório `EX3`

```
EX3/
├── app.py                     # Entrypoint da aplicação FastAPI e inclusão de rotas
├── cinema.py                  # Fachada (Facade) e sincronização com banco de dados
├── requirements.txt           # Lista de dependências do projeto
├── model/                     # Camada Model (entidades de domínio e persistência SQLite)
│   ├── database.py            # Conexão, helpers de execução e inicialização SQLite
│   ├── filme.py               # Modelo de Filme e schemas Pydantic
│   ├── sala.py                # Modelo de Sala e schemas Pydantic
│   ├── sessao.py              # Modelo de Sessão e schemas Pydantic
│   └── tipo_ingresso.py       # Modelo de Tipo de Ingresso e schemas Pydantic
├── controller/                # Camada Controller (regras de negócio e validações)
│   ├── filme_controller.py
│   ├── sala_controller.py
│   ├── sessao_controller.py
│   ├── tipo_ingresso_controller.py
│   ├── cadastraController.py
│   ├── buscaController.py
│   └── helpers/
│       └── validar_data.py
├── view/                      # Camada View (rotas REST HTTP e injeção de dependências)
│   ├── filme_view.py
│   ├── sala_view.py
│   ├── sessao_view.py
│   └── tipo_ingresso_view.py
└── tests/                     # Suíte de testes unitários e de integração por camada
    ├── test_model.py          # Testes unitários das entidades e schemas
    ├── test_controller.py     # Testes dos controllers e regras de negócio
    └── test_view.py           # Testes de integração dos endpoints REST FastAPI
```