
# Cloud Image Service

Serverless image upload and management service using AWS Lambda, S3, DynamoDB.
Runs fully locally using LocalStack.

## Prerequisites
- Docker + Docker Compose
- Python 3.8+
- AWS CLI

## Environment variables
```
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT=http://localhost:4566
```

## Run locally

docker-compose up
