# Wallet API Desafio em Python

Uma API REST simplificada para gerenciamento de carteira digital, usando FastAPI e armazenamento em memória. Versão didática para estudos.

## 🚀 Funcionalidades

- Cadastro e login de usuários
- Depósitos e saques
- Consulta de saldo
- Histórico de transações

## 🏗️ Estrutura do Projeto

O projeto possui uma estrutura simplificada:

```
wallet-py/
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py            # Configuração da API
    ├── router.py          # Rotas da API
    ├── models/
    │   ├── __init__.py
    │   └── models.py      # Classes e banco de dados em memória
    └── schemas/
        ├── __init__.py
        └── schemas.py     # Schemas de validação
```

## 🛠️ Tecnologias

- Python 3.8+
- FastAPI
- Pydantic
- Uvicorn

## 📋 Como Executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Inicie a aplicação:
```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## 📚 Endpoints e Como Usar

### 1. Criar Usuário
```powershell
$body = @{
    name = "João Silva"
    email = "joao@email.com"
    password = "senha123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/users/" -Method Post -Body $body -ContentType "application/json"
```

### 2. Login
```powershell
$loginBody = @{
    email = "joao@email.com"
    password = "senha123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/token" -Method Post -Body $loginBody -ContentType "application/json"
$token = $response.access_token
```

### 3. Depósito
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
}

$depositBody = @{
    amount = 100
    type = "deposit"
    description = "Depósito inicial"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/transactions/" -Method Post -Body $depositBody -ContentType "application/json" -Headers $headers
```

### 4. Saque
```powershell
$withdrawBody = @{
    amount = 30
    type = "withdrawal"
    description = "Saque teste"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/transactions/" -Method Post -Body $withdrawBody -ContentType "application/json" -Headers $headers
```

### 5. Consultar Saldo
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/balance/" -Method Get -Headers $headers
```

### 6. Listar Transações
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/transactions/" -Method Get -Headers $headers
```

## 📝 Observações

Esta é uma versão simplificada para estudos onde:
- Os dados são armazenados em memória (são perdidos ao reiniciar a aplicação)
- A autenticação é simplificada (sem criptografia de senha)
- O token é o próprio email do usuário mais podemos implementar um token mais seguro sei lá m jwt heh~

## 📚 Documentação Interativa

Para testar a API de forma interativa, acesse:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`