# {{cookiecutter.project_name}}

Dev stack:
* django 3
* django rest api
* celery
* uwsgi
* postgres
* redis
* docker

## Clone repository

Install git on your system https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

```
git clone ...
cd {{cookiecutter.project_slug}}
```

## Run using docker

Install docker on your system https://runnable.com/docker/getting-started/

### Activate environment:

```
cp envsets/docker_local.env envsets/.env
```

### Build and Run

```
docker-compose -f docker-compose-local.yml build
docker-compose -f docker-compose-local.yml up
```

## Run without docker

### Install required services (OSX)

```
brew install pyenv
brew install postgresql
brew install redis

brew services
brew services start postgresql
brew services start redis
```

### Install required services (Ubuntu)

```
apt...
```

### Setup pyenv

Please, execute these commands to activate your pyenv (for bash just replace .zshrc with .bashrc)

```
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
eval "$(pyenv init -)"
```

### Install and activate virtual environment

```
pyenv install 3.7.4
pyenv shell 3.7.4

python -mvenv env
source env/bin/activate
```

### Activate environment:

```
cp envsets/local.env envsets/.env
export envsets/.env
```

### Install project requirements:

```
pip install --upgrade pip
make install
```

### Prepare database:

```
createdb {{cookiecutter.db_name}}
python manage.py migrate
```

### Start dev server:

```
python manage.py makemigrations
make start
```

## Run tests:

### Run all tests:

```
make test
```

### Run one test:

```
pytest file/path/filename.py::test_method
```

## Apply db snapshot

```
psql -f db_2019-09-04_15\:48.sql {{cookiecutter.db_name}}
```

## Visualize DB

```
brew install graphviz
pip install pygraphviz
python manage.py graph_models -a -g -o {{cookiecutter.db_name}}.svg
```
