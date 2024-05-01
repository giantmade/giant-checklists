SHELL := /bin/bash
PROJECT = giant-checklists

githooks:
	git config core.hooksPath .githooks

test:
	DEPLOY_ENV=test python ./manage.py collectstatic --noinput
	DJANGO_SETTINGS_MODULE=core.settings DEPLOY_ENV=test pytest checklists

ci-test:
	python src/manage.py collectstatic --noinput
	set -o pipefail ; pytest --junitxml=pytest.xml --cov-report=term-missing:skip-covered --cov=src src | tee pytest-coverage.txt

lint:
	flake8 src
	black --check src

cleanup:
	black src
	isort src

requirements-freeze:
	docker-compose run web poetry export -f requirements.txt > ./etc/requirements.txt

docker-test:
	docker-compose run test src/manage.py collectstatic --noinput
	docker-compose run test pytest src

docker-ci-test:
	python src/manage.py collectstatic --noinput
	pytest --junitxml=pytest.xml --cov-report=term-missing:skip-covered --cov=src src | tee pytest-coverage.txt
	exit ${PIPESTATUS[0]}
