
test: OPTS ?= ""
test:
	python3 -m pytest $(OPTS) tests


coverage: OPTS ?= ""
coverage:
	python3 -m pytest $(OPTS) -vv --cov .
