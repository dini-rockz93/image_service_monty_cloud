from app.services.s3_service import delete_image
from app.services.dynamo_service import table
from app.utils.response import response

def handler(event, context):
    image_id = event["pathParameters"]["image_id"]
    user_id = event["headers"]["user-id"]
    delete_image(image_id)
    table.delete_item(Key={"user_id": user_id, "image_id": image_id})
    return response(204, {})
