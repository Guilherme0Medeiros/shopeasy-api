# 🛍️ ShopEasy API

ShopEasy é uma API RESTful desenvolvida com Django REST Framework para gerenciamento de um e-commerce. O sistema inclui funcionalidades como autenticação JWT, carrinho de compras, pedidos, produtos, e soft delete.

## 🚀 Funcionalidades

- ✅ Cadastro, edição e exclusão (soft delete) de produtos
- ✅ Adição e remoção de produtos no carrinho
- ✅ Geração de pedidos e pagamento
- ✅ Autenticação via JWT
- ✅ Paginação automática
- ✅ Filtros por status e campo `excluido`
- ✅ Documentação via Swagger e ReDoc

## 📦 Tecnologias utilizadas

- Python 3.13
- Django 5
- Django REST Framework
- drf-spectacular (Swagger docs)
- djangorestframework-simplejwt (JWT Auth)


## 📁 Estrutura do Projeto

```bash
ShopEasyApi/
├── manage.py
├── .env
├── requirements.txt
├── README.md
├── shopeasy/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── shop/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── tests.py
│   ├── apps.py
│   ├── migrations/
│   └── api/
│       └── v1/
│           ├── viewsets.py
│           ├── serializers.py
│           └── router.py
└── venv/
```

## 🔐 Autenticação

A API utiliza autenticação JWT. Para obter um token:

POST /api/v1/token/ { "username": "seu_usuario", "password": "sua_senha" }

Use o token no cabeçalho das requisições protegidas:

Authorization: Bearer <seu_token>

## 🔀 Endpoints principais

### Produtos

| Método | Endpoint             | Descrição                          |
|--------|----------------------|-----------------------------------|
| GET    | /api/v1/produtos/    | Lista produtos                    |
| POST   | /api/v1/produtos/    | Cria um novo produto              |
| PATCH  | /api/v1/produtos/:id | Atualiza produto                  |
| DELETE | /api/v1/produtos/:id | Soft delete no produto            |

### Carrinho

| Método | Endpoint                    | Descrição                                |
|--------|-----------------------------|-------------------------------------------|
| GET    | /api/v1/carrinhos/          | Detalhes do carrinho                     |
| POST   | /api/v1/carrinhos/adicionar-item/ | Adiciona item ao carrinho         |
| POST   | /api/v1/carrinhos/remover-item/  | Remove item do carrinho            |

### Pedidos

| Método | Endpoint             | Descrição                           |
|--------|----------------------|--------------------------------------|
| GET    | /api/v1/pedidos/     | Lista de pedidos                     |
| POST   | /api/v1/pedidos/     | Cria um novo pedido                  |
| POST   | /api/v1/pedidos/:id/pagar/ | Marca o pedido como pago         |
| DELETE | /api/v1/pedidos/:id/ | Soft delete no pedido                |

## 📚 Documentação

- Swagger: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- ReDoc: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)

## ⚙️ Como rodar o projeto

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/seu-repo.git

# Acessar a pasta
cd ShopEasyApi

# Criar e ativar ambiente virtual
# No Windows
python -m venv venv
venv\Scripts\activate

# No Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar migrações
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

## 🧪 Testes

Você pode usar ferramentas como Postman, Insomnia ou a própria interface Swagger para testar os endpoints.

