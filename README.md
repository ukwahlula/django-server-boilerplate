# Django server boilerplate

## Clone repository

Install git on your system https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

```
git clone ...
cd django-server-boilerplate
```

## Install required services (OSX)

```
brew install pyenv
```

## Install required services (Ubuntu)

```
apt...
```

## Setup pyenv

Please, execute these commands to activate your pyenv (for bash just replace .zshrc with .bashrc)

```
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
eval "$(pyenv init -)"
```

## Install and activate virtual environment

```
pyenv install 3.7.4
pyenv shell 3.7.4

python -mvenv env
source env/bin/activate
```

## Install project requirements:

```
pip install --upgrade pip
pip install -r requirements.txt
```


## Create your project:

```
cd ../
cookiecutter django-server-boilerplate
```
