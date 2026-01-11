import base64
from app.services.s3_service import get_image

def handler(event, context):
    obj = get_image(event["pathParameters"]["image_id"])
    return {
        "statusCode": 200,
        "isBase64Encoded": True,
        "body": base64.b64encode(obj["Body"].read()).decode()
    }
