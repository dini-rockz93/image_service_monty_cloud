
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


## Local AWS Resource Setup (LocalStack)

Before running the application or tests, ensure the required AWS resources are available in LocalStack.

Create and verify the S3 bucket
```
aws --endpoint-url=http://localhost:4566 s3 mb s3://image-bucket
aws --endpoint-url=http://localhost:4566 s3 ls
```

![aws s3 setup](images/aws_s3.png)

Create and verify the DynamoDB table

```
aws --endpoint-url=http://localhost:4566 dynamodb create-table \
  --table-name ImagesTable \
  --attribute-definitions \
    AttributeName=user_id,AttributeType=S \
    AttributeName=image_id,AttributeType=S \
  --key-schema \
    AttributeName=user_id,KeyType=HASH \
    AttributeName=image_id,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST
aws --endpoint-url=http://localhost:4566 dynamodb list-tables
```

![aws dynamodb setup](images/aws_dynamo.png)

ℹ️ These steps are required only if the LocalStack initialization script has not already provisioned the resources.

## Run locally

```
docker-compose up
```

![LocalStack Running](images/docker_ready.png)

## Run pytest

``` 
pytest tests/test_smoke.py -v 
```

![pytest success](images/pytest.png)