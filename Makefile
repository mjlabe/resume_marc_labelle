CONFIG ?= resume.ini

build:
	docker-compose build

build-static: config
	docker-compose run resume-web resume-to-pdf ${CONFIG}

config:
	CONFIG=${CONFIG} \
	docker-compose config

shell:
	docker-compose run resume-web bash

up: config
	CONFIG=${CONFIG} \
		docker-compose up resume-web

down:
	docker-compose down

test:
	pytest
