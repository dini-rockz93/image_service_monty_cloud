
import boto3, uuid, os
from botocore.exceptions import ClientError
from app.utils.retry import retry

s3 = boto3.client("s3", endpoint_url=os.getenv("AWS_ENDPOINT"))
BUCKET = "image-bucket"

@retry((ClientError,))
def upload_image(data, content_type):
    image_id = str(uuid.uuid4())
    s3.put_object(Bucket=BUCKET, Key=image_id, Body=data, ContentType=content_type)
    return image_id

@retry((ClientError,))
def get_image(image_id):
    return s3.get_object(Bucket=BUCKET, Key=image_id)

@retry((ClientError,))
def delete_image(image_id):
    s3.delete_object(Bucket=BUCKET, Key=image_id)
