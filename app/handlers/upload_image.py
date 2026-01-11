import base64, json
from app.services.s3_service import upload_image
from app.services.dynamo_service import save_metadata
from app.utils.response import response

def handler(event, context):
    body = json.loads(event["body"])
    user_id = event["headers"]["user-id"]
    image = base64.b64decode(body["file"])
    metadata = body["metadata"]
    image_id = upload_image(image, metadata["content_type"])
    save_metadata(user_id, image_id, metadata)
    return response(200, {"image_id": image_id})
