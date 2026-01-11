from app.services.dynamo_service import list_by_user
from app.utils.response import response

def handler(event, context):
    user_id = event["queryStringParameters"]["user_id"]
    return response(200, list_by_user(user_id))
