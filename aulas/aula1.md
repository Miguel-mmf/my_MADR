# Anotações - Aula 1 - Configurando o Ambiente de Desenvolvimento


## Instalação do Python

Para a configuração do ambiente de desenvolvimento em Python, será utilizado o [**pyenv**](https://pyenv-win.github.io/pyenv-win/).

> Pyenv é uma aplicação externa ao python que permite que você instale diferentes versões do python no sistema e as isola. Podendo isolar versões específicas, para projetos específicos.

Para instalar o pyenv no linux, utilize o comando abaixo
```bash
curl https://pyenv.run | bash
```

Para instalar o pyenv no windows, clique [aqui](https://pyenv-win.github.io/pyenv-win/).

Uma vez que o pyenv esteja instalado na máquina, execute o comando a seguir

```bash
pyenv update
pyenv install 3.11:latest
```

Para verificar qual a versão instalada do pyenv, utilize o comando

```bash
pyenv --version
```

Da mesma forma para o python, apenas substitua o comando pyenv pela chamada `python --version`.

Para verificar as versões do Python disponíveis para utilizar via pyenv, utilize o comando
```bash
pyenv versions
```

## Instalando o `pipx`

O pipx permite que você instale e execute aplicações em python em ambientes isolados na sua máquina.

Para instalar no linux, execute o comando abaixo
```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
```

Para instalar no windows, acesse o [link](https://github.com/pypa/pipx#on-windows).

Para que a versão do python que instalamos via pyenv seja usada em nosso projeto criado com poetry, devemos dizer ao pyenv qual versão do python será usada nesse diretório
```bash
pyenv local 3.11.9
```

## Gerenciamento de dependências com o Poetry

O Poetry é um gerenciador de pacotes e dependências para Python. O Poetry facilita a criação, o gerenciamento e a distribuição de pacotes Python.

Para instalar o poetry no ambiente virtual, utilize o comando
```python
pipx install poetry
```

Para criar um projeto com o poetry, utilize o comando
```python
poetry new fast_zero
```

Para instalar e configurar o projeto com o poetry, utilize o comando
```python
poetry install
```

Esse comando já vai criar um poetry.lock no mesmo diretório.

Para adicionar dependências a um projeto com o poetry, utilize o comando
```python
poetry add <nome da dependência>
```

Para adicionar uma dependência de desenvolvimento, como o pytest, e excluir essas dependências do projeto em produção, utiliza-se grupos com o comando abaixo

```bash
poetry add --group dev pytest pytest-cov taskipy ruff httpx

```
No comando acima, os pacotes pytest pytest-cov taskipy ruff httpx estão sendo adicionados ao projeto como dependências de desenvolvimento e, portanto, não estão no **[tool.poetry.dependencies]** no arquivo **pyproject.toml**.

## Primeiro *Hello, World!*

Uma coisa bastante interessante sobre o FastAPI é que ele é um framework web baseado em funções. Da mesma forma em que criamos funções tradicionalmente em python, podemos estender essas funções para que elas sejam servidas pelo servidor.

```python
def read_root():
    return {'message': 'Hello, World!'}
```

Desta forma, usando somente um decorador do FastAPI, podemos fazer com que uma determinada função seja acessível pela rede:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Hello, World!'}

```

## Analisador estático de código [ruff](https://docs.astral.sh/ruff/)

Neste projeto, a ferramenta **ruff** será usada com duas finalidades, sendo essas:
* Um analisador estático de código (um linter), para dizer se não estamos infringido alguma boa prática de programação;
* Um formatador de código. Para seguirmos um estilo único de código. Vamos nos basear na PEP-8.

Para analisar um arquivo em específico, utilize o comando

```bash
ruff check <arquivo>

```

Para aplicar todas as regras (disponível no arquivo ***pyproject.toml*** em **[tool.ruff.format]**) e formartar o arquivo com erros, utilize o comando

```bash
ruff format <arquivo>

```

### Cobertura de código com o [pytest](https://docs.pytest.org/)

O Pytest é uma framework de testes, que usaremos para escrever e executar nossos testes. O configuraremos para reconhecer o caminho base para execução dos testes na raiz do projeto `.`.


### Executor de tarefas [taskipy](https://github.com/taskipy/taskipy)

A ideia do Taskipy é ser um executor de tarefas (task runner) complementar em nossa aplicação. É um alias.

Para listar todos os *alias* disponíveis, isto é, cadastrados na tabela **[tool.taskipy.tasks]** no arquivo **pyproject.toml**.

```bash
task -l

```

