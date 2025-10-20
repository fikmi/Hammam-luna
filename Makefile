.PHONY: install dev run test lint format seed

install:
pip install -e .

dev:
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

run:
python manage.py runserver 0.0.0.0:8000

test:
pytest --maxfail=1

lint:
ruff check .

format:
black .
ruff check --fix .

seed:
python manage.py seed_demo
