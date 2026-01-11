import json
from app.services.s3_service import upload_image
from app.services.dynamo_service import save_metadata
from app.utils.response import success, error
from app.utils.validators import validate_image_upload
from app.utils.errors import BadRequestError

def handler(event, context):
    try:
        if "body" not in event:
            raise BadRequestError("Missing request body")

        body = json.loads(event["body"])
        headers = event.get("headers", {})

        user_id = headers.get("user-id")
        if not user_id:
            raise BadRequestError("Missing user-id header")

        metadata = body.get("metadata", {})
        content_type = metadata.get("content_type")

        if not content_type:
            raise BadRequestError("content_type is required")

        # ✅ STRICT IMAGE VALIDATION
        image_bytes = validate_image_upload(
            body.get("file"),
            content_type
        )

        image_id = upload_image(image_bytes, content_type)
        save_metadata(user_id, image_id, metadata)

        return success(200, {"image_id": image_id})

    except Exception as e:
        return error(e)
