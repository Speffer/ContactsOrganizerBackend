# Contact List -  API REST

> A Flask RESTful project

## Primeiros Passos

``` bash
# Requerimentos para rodar
Python 3.5+ - https://www.python.org/

# Após clonar e entrar na pasta do projeto rodar:
pip install virtualenv (caso não tenha instalado)
python -m venv venv

# Para ativar no windows:
./venv/Scripts/activate.bat

# Para ativar no Linux/Mac:
source venv/bin/activate

# Após criar e ativar a virtualenv rodar:
pip install requirements.txt

# Para criar nosso banco de dados rode os seguintes comandos em sequencia:
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

# Para servir a API localmente
python app.py

```
