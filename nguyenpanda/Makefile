mypy:
	@echo "\033[1;92mmypy is checking package: \033[1;96mnguyenpanda\033[0m"; \
	mypy -p nguyenpanda; \
	echo "\033[1;92mmypy is checking with package: \033[1;96m__tests\033[0m"; \
	mypy __tests

TEST_FILES := butterfly.py owl.py swan.py
test_all:
	@test_root_directory=__tests/; \
	for file in $(TEST_FILES); do \
		echo "\033[1;92mTest Python file: \033[1;96m$${test_root_directory}$$file\033[0m"; \
		python $${test_root_directory}$$file; \
	done

big_check: test_all mypy

local:
	@echo "\033[1;92mpip install -e\033[0m"
	@pip install -e .

pypi:
	python setup.py sdist bdist_wheel
	python -m twine upload --verbose dist/*

pack:
	pip freeze --local

work:
	@echo "\033[1;92mYes! You can run \033[1;96mmakefile\033[1;92m in terminal!!!\033[0m"

# pip freeze --local | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U