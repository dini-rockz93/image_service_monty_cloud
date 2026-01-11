import json
from app.handlers.upload_image import handler

def test_reject_large_file():
    large_data = "a" * (6 * 1024 * 1024)  # >5MB

    event = {
        "headers": {"user-id": "test-user"},
        "body": json.dumps({
            "file": large_data,
            "metadata": {
                "filename": "big.jpg",
                "content_type": "image/jpeg"
            }
        })
    }

    response = handler(event, None)
    assert response["statusCode"] == 400


def test_reject_invalid_signature():
    fake_png = "dGVzdA=="  # base64("test")

    event = {
        "headers": {"user-id": "test-user"},
        "body": json.dumps({
            "file": fake_png,
            "metadata": {
                "filename": "fake.png",
                "content_type": "image/png"
            }
        })
    }

    response = handler(event, None)
    assert response["statusCode"] == 400
