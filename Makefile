.ONESHELL:

.PHONY: clean install initdb test cov dev run

clean:
		find . -type f -name '*.pyc' -delete
		find . -type f -name '*.log' -delete
		find . -type f -name '*.db' -delete

install:
		python3 -m venv venv; \
		. venv/bin/activate; \
		pip install -r requirements.txt; \
		python3 init_db.py

initdb:
		. venv/bin/activate; \
		python3 init_db.py

test:
		. venv/bin/activate; \
		python -m pytest tests/ -W ignore::DeprecationWarning

cov:
		. venv/bin/activate; \
		python -m pytest tests/ -W ignore::DeprecationWarning --cov=app

dev:
		. venv/bin/activate; \
		export FLASK_APP=app; \
		export FLASK_ENV=development; \
		python3 -m flask run --host=0.0.0.0 --port=8000

run:
		. venv/bin/activate; \
		export FLASK_APP=app; \
		export FLASK_ENV=production; \
		python3 -m flask run --host=0.0.0.0 --port=80