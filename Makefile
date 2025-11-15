REGION ?= us-east-1
ACCOUNT_ID ?= 123456789012
TAG ?= latest

.PHONY: build-users push-users build-auth push-auth all
#.PHONY: build-users push-users

build-users:
	 docker build -t users-service:$(TAG) ./users

push-users: build-users
	 aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com
	 docker tag users-service:$(TAG) $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/users-service:$(TAG)
	 docker push $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/users-service:$(TAG)

build-auth:
	 docker build -t auth-service:$(TAG) ./auth

push-auth: build-auth
	 aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com
	 docker tag auth-service:$(TAG) $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/auth-service:$(TAG)
	 docker push $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/auth-service:$(TAG)

all: push-users push-auth
#all: push-users
