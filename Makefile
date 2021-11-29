# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* football_stats/*.py

black:
	@black scripts/* football_stats/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr football_stats-*.dist-info
	@rm -fr football_stats.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

# ----------------------------------
#      		API & UI
# ----------------------------------
IMAGE_NAME=football_stats
PROJECT_ID=wagon-bootcamp-332313
DOCKER_IMAGE_NAME = football_stats
REGION=eu.gcr.io
run_streamlit:
	streamlit run app.py

run_api:
	uvicorn api.fast:app --reload

build_image:
	docker build --tag=$(REGION)/$(PROJECT_ID)/$(DOCKER_IMAGE_NAME) .

run_image:
	docker run -it -e PORT=8000 -p 8000:8000 $(REGION)/$(PROJECT_ID)/$(DOCKER_IMAGE_NAME)

docker_push:
	docker push $(REGION)/$(PROJECT_ID)/$(DOCKER_IMAGE_NAME)

gcp_deploy:
	gcloud run deploy --image $(REGION)/$(PROJECT_ID)/$(DOCKER_IMAGE_NAME) --platform managed --region europe-west1
