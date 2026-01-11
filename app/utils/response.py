import json
from decimal import Decimal
from app.utils.errors import AppError

def _json_serializer(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def success(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=_json_serializer),
    }

def error(err: Exception):
    if isinstance(err, AppError):
        return {
            "statusCode": err.status_code,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(err.to_dict()),
        }

    return {
        "statusCode": 500,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": "Unexpected server error"}),
    }
