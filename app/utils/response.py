import json
from decimal import Decimal

def _json_serializer(obj):
    if isinstance(obj, Decimal):
        # DynamoDB numbers come as Decimal
        if obj % 1 == 0:
            return int(obj)
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=_json_serializer),
    }
