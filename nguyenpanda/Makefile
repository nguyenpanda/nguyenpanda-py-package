work!:
	@echo "\033[1;92mYes! You can run \033[1;96mmakefile\033[1;92m in terminal!!!\033[0m"

test:
	@test_root_directory=__tests/; \
	echo "\033[1;92mTest Python file: $${test_root_directory}$(file)\033[0m"; \
	python $${test_root_directory}$(file)

run:
	@echo "\033[1;92mCommitting package to local\033[0m"
	@cd .. && pip install -e . && cd nguyenpanda

lsPack:
	pip freeze --local

# pip freeze --local | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U