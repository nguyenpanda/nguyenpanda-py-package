# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

pypi:
	@echo "\033[1;92Updata pip, build, twine\033[0m"
	python3 -m pip install --upgrade pip
	python3 -m pip install --upgrade build
	python3 -m pip install --upgrade twine
	@echo "\033[1;92Building distribution files\033[0m"
	python3 -m build
	@echo "\033[1;92Upload to PyPi\033[0m"
	python3 -m twine upload --repository pypi dist/*

.DEFAULT_GOAL := help

<caret>

.PHONY: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)