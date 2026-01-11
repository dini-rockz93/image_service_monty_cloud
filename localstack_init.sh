
#!/bin/bash
set -e
awslocal s3 mb s3://image-bucket || true
awslocal dynamodb create-table   --table-name ImagesTable   --attribute-definitions     AttributeName=user_id,AttributeType=S     AttributeName=image_id,AttributeType=S     AttributeName=tag,AttributeType=S     AttributeName=created_at,AttributeType=N   --key-schema     AttributeName=user_id,KeyType=HASH     AttributeName=image_id,KeyType=RANGE   --global-secondary-indexes '[
    {
      "IndexName": "TagIndex",
      "KeySchema": [
        {"AttributeName": "tag", "KeyType": "HASH"},
        {"AttributeName": "created_at", "KeyType": "RANGE"}
      ],
      "Projection": {"ProjectionType": "ALL"}
    },
    {
      "IndexName": "UserDateIndex",
      "KeySchema": [
        {"AttributeName": "user_id", "KeyType": "HASH"},
        {"AttributeName": "created_at", "KeyType": "RANGE"}
      ],
      "Projection": {"ProjectionType": "ALL"}
    }
  ]'   --billing-mode PAY_PER_REQUEST || true
