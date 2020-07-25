# Teste Prático Backend

API REST, feita utilizando o microframework Flask, com autenticação via JWT para cadastro de produtos. A API suporta os métodos **GET**, **POST**, **PUT** e **DELETE**. Os dados dos usuários e produtos são persistidos em base MySQL.  A API possui cobertura de testes unitários.

**Versão do Python utilizada:**
Python 3.6

## Instalação
```bash
# Clone o repositório
$ git clone https://github.com/marcossilvaxx/teste_backend.git

# Acesse o diretório do projeto
$ cd ./teste_backend

# Crie e ative seu virtualenv (opcional)
$ python -m venv venv

	# Ativando no Linux
	$ source venv/bin/activate

	# Ativando no Windows
	$ venv\Scripts\activate

# Instale as dependências:
$ pip install -r requirements.txt
 
```

## Configuração

No arquivo localizado em `app/config.py`, altere os valores das variáveis `SECRET_KEY` e `SQLALCHEMY_DATABASE_URI` de acordo com sua preferência e configuração:

```python
DEBUG = True  # In production mode, change to False
SECRET_KEY = "SUA_CHAVE_DE_SEGURANÇA" # Chave de segurança para gerar os hashes da aplicação
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:senha@servidor:porta/nomedobanco' # String de conexão do banco de dados
SQLALCHEMY_TRACK_MODIFICATIONS = False
``` 

## Preparando o banco de dados

Para criar as tabelas do banco de dados, execute as **migrations** com o comando:

```bash
$ flask db upgrade
```

## Rodando o servidor

Para rodar o servidor, estando no diretório raiz do projeto, execute o seguinte comando:

```bash
$ python run.py
```

## Endpoints da API

### /auth/register (POST)
**Descrição:** Cadastra um usuário no banco de dados.
```
POST /auth/register
```
**Exemplo de corpo da requisição (JSON):**
```json
{
	"name": "Marcos",
	"email": "marcos@email.com",
	"password": "12345"
}
```
**Exemplo de retorno:**
```json
{
	"message": "User successfully registered!"
}
```

### /auth/login (POST)
**Descrição:** Realiza a autenticação de um usuário já cadastrado. Retorna um token com tempo de expiração de 10 minutos para realizar requisições nas rotas privadas.
```
POST /auth/login
```
**Exemplo de corpo da requisição (JSON):**
```json
{
	"email": "marcos@email.com",
	"password": "12345"
}
```
**Exemplo de retorno:**
```json
{
	"token": "ALGUM_TOKEN_AQUI"
}
```

### /products (GET)
**Descrição:** Retorna uma lista de todos os produtos cadastros.
```
GET /products
```

**Exemplo de retorno:**
```json
[
	{
		"name": "feijão",
		"price": 6.55,
		"cost": 3.35
	},
	{
		"name": "arroz",
		"price": 4.0,
		"cost": 2.55
	}
]
```

### /products (POST)
**Descrição:** Recebe um produto em formato JSON e cadastra ele no banco de dados.
```
POST /products
```
**Exemplo de corpo da requisição (JSON):**
```json
{
	"name": "feijão",
	"price": 6.55,
	"cost": 3.35
}
```
**Exemplo de retorno:**
```json
{
	"message": "Product was registered"
}
```

### /products/{id} (PUT)
**Descrição:** Recebe campos (é possível receber alguns ou todos) de um produto em formato JSON e atualiza o produto com o id (no endpoint) correspondente no banco de dados.
```
PUT /products/{id}
```
**Exemplo de corpo da requisição (JSON):**
```json
// Exemplo de requisição: PUT /products/1

{
	"price": 10.45,
	"cost": 5.99
}
```
**Exemplo de retorno:**
```json
{
	"message": "Product was updated"
}
```

### /products/{id} (DELETE)
**Descrição:** Remove o produto com o id (no endpoint) correspondente no banco de dados.
```
DELETE /products/{id}
```
**Exemplo de retorno:**
```json
// Exemplo de requisição: DELETE /products/1

{
	"message": "Product was removed"
}
```

## Rodando os testes

**OBS:** Mockar objetos do banco (flask-sqlalchemy) é bastante complexo. Para contornar isso, usei uma prática recomendada na própria documentação do Flask:

 1. No início da execução dos testes é criado um banco de dados SQLite (temporário) APENAS para os testes.
 2. Durante a execução dos testes são criados registros **falsos** (para testagem) no banco SQLite.
 3. Ao fim de todos os testes, o banco de dados SQLite é apagado.

Para rodar os testes, esteja localizado no diretório raiz do projeto e execute o seguinte comando no terminal:
```bash
$ py.test
```
---
Feito por [Marcos Silva](https://github.com/marcossilvaxx)
