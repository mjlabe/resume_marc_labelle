CONFIG ?= resume.ini
RESUME ?= staff

build:
	docker-compose build

resume: build config
	docker-compose run resume-web resume-to-pdf ${CONFIG} --content-file ${RESUME}

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
