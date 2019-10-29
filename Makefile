help:                         ## Print help
	@grep -e "##" Makefile | grep -v "grep"

clean:                        ## Remove artifacts
	@find . -path '*_pycache_*' -prune -exec rm -rf {} \;
	@find . -name '.DS_Store' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;
	@find . -name '\#*\#' -exec rm -rf {} \;
	@rm -rf .pytest_cache .coverage htmlcov

lint:                         ## Check PEP8 compliance and code style
	@pylint ./winbot
	@pycodestyle ./winbot

prcheck: lint                 ## Perform all necessary code checks
