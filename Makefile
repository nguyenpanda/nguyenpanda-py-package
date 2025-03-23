mypy:
	@echo "\033[1;92mmypy is checking package: \033[1;96mnguyenpanda\033[0m"
	mypy src/nguyenpanda

local:
	@echo "\033[1;92mpip install -e\033[0m"
	@pip install -e .

build:
	@echo "\033[1;92mBuilding distribution files\033[0m"
	python3 setup.py bdist_wheel sdist

test_pypi: build
	@echo "\033[1;92mUploading to Test PyPi\033[0m"
	python3 -m twine upload --repository testpypi dist/*

pypi: build
	@echo "\033[1;92mUploading to PyPi\033[0m"
	python3 -m twine upload --repository pypi dist/*

pack:
	pip freeze --local
