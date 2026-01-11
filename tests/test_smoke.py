import base64
import json
import time
import boto3
import os

from app.handlers.upload_image import handler as upload_handler
from app.handlers.list_images import handler as list_handler
from app.handlers.get_image import handler as get_handler
from app.handlers.delete_image import handler as delete_handler

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localhost:4566")
REGION = "us-east-1"

USER_ID = "test-user"
TEST_IMAGE_BYTES = b"this-is-a-fake-image"

def test_localstack_services_exist():
    s3 = boto3.client("s3", endpoint_url=AWS_ENDPOINT, region_name=REGION)
    ddb = boto3.client("dynamodb", endpoint_url=AWS_ENDPOINT, region_name=REGION)

    buckets = s3.list_buckets()["Buckets"]
    tables = ddb.list_tables()["TableNames"]

    assert any(b["Name"] == "image-bucket" for b in buckets)
    assert "ImagesTable" in tables


def test_full_image_lifecycle():
    # -----------------------
    # Upload image
    # -----------------------
    upload_event = {
        "headers": {"user-id": USER_ID},
        "body": json.dumps({
            "file": base64.b64encode(TEST_IMAGE_BYTES).decode(),
            "metadata": {
                "filename": "test.jpg",
                "content_type": "image/jpeg",
                "tags": ["smoke"]
            }
        })
    }

    upload_response = upload_handler(upload_event, None)
    assert upload_response["statusCode"] == 200

    body = json.loads(upload_response["body"])
    image_id = body["image_id"]
    assert image_id is not None

    time.sleep(0.2)  # allow DynamoDB consistency

    # -----------------------
    # List images
    # -----------------------
    list_event = {
        "queryStringParameters": {"user_id": USER_ID}
    }

    list_response = list_handler(list_event, None)
    assert list_response["statusCode"] == 200

    images = json.loads(list_response["body"])
    assert any(img["image_id"] == image_id for img in images)

    # -----------------------
    # Download image
    # -----------------------
    get_event = {
        "pathParameters": {"image_id": image_id}
    }

    get_response = get_handler(get_event, None)
    assert get_response["statusCode"] == 200

    downloaded = base64.b64decode(get_response["body"])
    assert downloaded == TEST_IMAGE_BYTES

    # -----------------------
    # Delete image
    # -----------------------
    delete_event = {
        "headers": {"user-id": USER_ID},
        "pathParameters": {"image_id": image_id}
    }

    delete_response = delete_handler(delete_event, None)
    assert delete_response["statusCode"] == 204
