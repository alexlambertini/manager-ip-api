# IP Manager

**IP Manager** é uma API desenvolvida com **FastAPI** para o gerenciamento de endereços IP.  
Ela permite verificar se os IPs estão ativos (online/offline), agrupar IPs por categorias e fornecer links externos definidos pelo usuário para cada IP.

## Funcionalidades

- Verificação de status (ping) de IPs: identifica se estão online ou offline.
- Associação de links externos a cada IP.
- Organização de IPs por grupos personalizados.
- Sistema de autenticação simples via variáveis de ambiente.

## Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- Python 3.9+

## Configuração de Autenticação

O sistema de login é baseado em credenciais fixas configuradas via arquivo `.env`.  
Crie um arquivo `.env` na raiz do projeto com os seguintes dados:

```bash
API_USER=seu_usuario
API_PASS=sua_senha
```

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/alexlambertini/manager-ip-api.git
cd manager-ip-api
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Inicie o servidor de desenvolvimento:

```bash
uvicorn main:app --reload
```

A API estará disponível em: http://localhost:8000
Para acessar o Swegger: http://localhost:8000/docks

## EN

# IP Manager

**IP Manager** is an API developed using **FastAPI** for managing IP addresses.  
It allows you to check the online/offline status of IPs (via ping), group IPs by category, and associate external links with each IP.

## Features

- Ping check to determine if an IP is online or offline.
- Add custom external links for each IP.
- Organize IPs into user-defined groups.
- Simple login system using environment variables.

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- Python 3.9+

## Authentication Setup

The login system uses static credentials set in a `.env` file.  
Create a `.env` file in the root of the project with the following contents:

```bash
API_USER=seu_usuario
API_PASS=sua_senha
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/alexlambertini/manager-ip-api.git
cd manager-ip-api
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at: http://localhost:8000
Swagger documentation: http://localhost:8000/docs
