.PHONY: pip-freeze uv-install uv-sync uv-lock uv-tree uv-outdated test format lint check

## ATTENTION! activate virtual environment before running!

## Install all dependencies
uv-install:
	uv sync

## Install dev dependencies
uv-sync-dev:
	uv sync --extra dev

## pip freeze
pip-freeze:
	uv pip list

## Show dependency tree
uv-tree:
	uv tree

## Show outdated packages
uv-outdated:
	uv pip list --outdated

## Update lock file
uv-lock:
	uv lock

## Full sync with lock file update
uv-sync:
	uv sync

## Run checks without fixing
check:
	uv run mypy src
	uv run ruff check .
## Run tests with coverage
test:
	uv run pytest --cov=src --cov-report=term-missing

## Format code
format:
	uv run ruff format .

## Lint code
lint:
	uv run ruff check . --fix

## Show uv version and info
uv-info:
	uv --version
	uv python list

## Clean cache
uv-clean:
	uv cache clean

## Export requirements.txt
uv-export:
	uv export --format requirements-txt --output-file requirements.txt

## Export dev requirements
uv-export-dev:
	uv export --format requirements-txt --group dev --output-file requirements-dev.txt


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################
.DEFAULT_GOAL := help
# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
#   * save line in hold space
#   * purge line
#   * Loop:
#       * append newline + line to hold spaceg
#       * go to next line
#       * if line starts with doc comment, strip comment character off and loop
#   * remove target prerequisites
#   * append hold space (+ newline) to line
#   * replace newline plus comments by `---`
#   * print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
