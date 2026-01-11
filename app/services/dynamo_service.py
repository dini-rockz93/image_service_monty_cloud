import boto3
import os
import time
from botocore.exceptions import ClientError
from app.utils.retry import retry

dynamodb = boto3.resource("dynamodb", endpoint_url=os.getenv("AWS_ENDPOINT"))
table = dynamodb.Table("ImagesTable")

@retry((ClientError,))
def save_metadata(user_id, image_id, metadata):
    for tag in metadata.get("tags", ["_none"]):
        table.put_item(Item={
            "user_id": user_id,
            "image_id": image_id,
            "tag": tag,
            "filename": metadata["filename"],
            "content_type": metadata["content_type"],
            "created_at": int(time.time())
        })

def list_by_user(user_id):
    return table.query(
        KeyConditionExpression="user_id = :u",
        ExpressionAttributeValues={":u": user_id}
    )["Items"]
