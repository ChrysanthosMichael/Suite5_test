-include .env
SHELL := /bin/bash

init-env:
	# bash templating engine to preserve existing env vars
	cat .env | sed -Ee "s/([\`\(|)\'\", <>\\\!\\\&])/\\\\\1/g" | sed -Ee "s/\\$$\\$$/\\\\$$\\\\$$/g" > .env.temp
	cat .env.template | sed -Ee "s/^/echo /g" | sed -Ee "s/([\`\(|)\'\",<>#])/\\\\\1/g" | sed -Ee "s/\\$$\\$$/\\\\$$\\\\$$/g" >> .env.temp
	cat .env.temp | bash > .env
	rm -f .env.temp
	if [ "$$(echo $${OSTYPE} | cut -c-6)" = "darwin" ]; then sed -i "" -e "s/sha256sum/shasum -a 256/g" .env; fi

create-requirements:
	. venv/bin/activate && pip list --format=freeze > requirements.txt

load-requirements:
	if [ -f requirements.txt ]; then \
		. venv/bin/activate && pip install -r requirements.txt; \
	else \
		echo "requirements.txt missing"; \
	fi

venv-init:
	python3 -m venv venv
	. venv/bin/activate && make load-requirements
	
run:
	. venv/bin/activate && \
	export FLASK_APP=${FLASK_APP} && \
	export FLASK_ENV=${FLASK_ENV} && \
	flask run --port ${FLASK_PORT}

run-background:
	. venv/bin/activate && \
	export FLASK_APP=${FLASK_APP} && \
	export FLASK_ENV=${FLASK_ENV} && \
	flask run --port ${FLASK_PORT} &

test:
	make clear-migrations
	make test-migrate
	. venv/bin/activate &&  pytest -vv tests/test.py

test-migrate:
	rm -rf ./app/app.db
	rm -rf ./migrations
	. venv/bin/activate && \
	flask db init && \
	flask db migrate && \
	flask db upgrade

clear-migrations:
	rm -rf ./app/app.db
	rm -rf ./migrations

init-db:
	. venv/bin/activate && \
	flask db init

migrate-up:
	. venv/bin/activate && \
	flask db migrate && \
	flask db upgrade

migrate-down:
	. venv/bin/activate && \
	flask db downgrade

dry_run:
	make venv-init && \
	make init-env && \
	make init-db && \
	make migrate-up && \
	make run \
