REPO = winbot
REPOURI = 882455274600.dkr.ecr.us-east-1.amazonaws.com
PROFILE = atlantic
REGION = us-east-1
AWSARGS = --region $(REGION) --no-include-email
SSH_PRIVATE_KEY:=$(shell cat ~/.ssh/dang_deployer_rsa)

help:                         ## Print help
	@grep -e "##" Makefile | grep -v "grep"

auth:                         ## Authenticate with AWS
	@rm -f /tmp/_tf_auth_batch.txt
	@rm -f /tmp/_aws_auth_batch.sh
	@read -p "Enter your MFA token > " mfa_token && \
	aws sts get-session-token --serial-number "$$(aws sts get-caller-identity --output text --query 'Arn' | sed "s/\:user\//\:mfa\//")" --token-code "$$mfa_token" --profile atlantic-data --output text > /tmp/_tf_auth_batch.txt && \
	echo "export AWS_ACCESS_KEY_ID=\"$$(cut -f2 /tmp/_tf_auth_batch.txt)\"" > /tmp/_aws_auth_batch.sh && \
	echo "export AWS_SECRET_ACCESS_KEY=\"$$(cut -f4 /tmp/_tf_auth_batch.txt)\""  >> /tmp/_aws_auth_batch.sh && \
	echo "export AWS_SESSION_TOKEN=\"$$(cut -f5 /tmp/_tf_auth_batch.txt)\"" >> /tmp/_aws_auth_batch.sh && \
	echo "export PS1=\"☁️  \033[0;31m[data-prod]\033[0m \$$PS1\"" >> /tmp/_aws_auth_batch.sh
	@rm -f /tmp/_tf_auth_batch.txt
	@echo "Run the following command to export temporary credentials to your envrionment: \n"
	@echo "source /tmp/_aws_auth_batch.sh && rm -f /tmp/_aws_auth_batch.sh"

run: build                    ## Run Docker image
	docker run -it --rm $(REPO)

build:                        ## Build Docker image
	@docker build -t $(REPO) --build-arg SSH_PRIVATE_KEY="$(SSH_PRIVATE_KEY)" .

shell: build                  ## Docker image shell
	docker run -it $(REPO) /bin/bash

push: build                   ## Push Docker image
	eval `aws ecr get-login $(AWSARGS)`
	$(eval BRANCH := $(shell git rev-parse --abbrev-ref HEAD))
	docker tag $(REPO) $(REPOURI)/$(REPO):$(BRANCH)
	docker push $(REPOURI)/$(REPO):$(BRANCH)

clean-all:                    ## Clear Docker cache
	docker system prune -a

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
