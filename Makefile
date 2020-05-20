
test: OPTS ?= ""
test:
	python3 -m pytest $(OPTS) tests
