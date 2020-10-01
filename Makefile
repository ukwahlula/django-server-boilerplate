clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + > /dev/null 2>&1
	find . -type f -name "*.pyc" -exec rm -rf {} + > /dev/null 2>&1

lint:
	flake8 --show-source .

all: clean lint

fix:
	black .
	isort -rc .
