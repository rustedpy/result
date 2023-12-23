# phony trick from https://keleshev.com/my-book-writing-setup/
.PHONY: phony

install: phony
ifndef VIRTUAL_ENV
	$(error install can only be run inside a Python virtual environment)
endif
	@echo Installing dependencies...
	pip install -r requirements-dev.txt
	pip install -e .

lint: phony lint-flake lint-mypy

lint-flake: phony
	flake8

lint-flake-pre310: phony
	# Python <3.10 doesn't support pattern matching.
	flake8 --extend-exclude tests/test_pattern_matching.py

lint-mypy: phony
	mypy

test: phony
	pytest

docs: phony
	lazydocs \
		--overview-file README.md \
		--src-base-url https://github.com/rustedpy/result/blob/master/ \
		./src/result
