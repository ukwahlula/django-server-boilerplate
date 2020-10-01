clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + > /dev/null 2>&1
	find . -type f -name "*.pyc" -exec rm -rf {} + > /dev/null 2>&1

install:
	pip install -r requirements/local.txt
	pre-commit install

celery:
	celery -A config worker -l INFO --purge --without-gossip --without-mingle --without-heartbeat -Q celery,emails

start:
	python manage.py collectstatic --noinput
	python manage.py migrate --noinput
	python manage.py initcontent
	python manage.py runserver 0.0.0.0:8000

lint:
	flake8 --show-source apps

test:
	flake8 --show-source apps
	isort --check-only -rc apps --diff
	python manage.py makemigrations --dry-run --check
	pytest --cov=apps --cov-report=term --cov-report=html -n 5

all: clean lint

fix:
	black apps
	isort -rc apps
