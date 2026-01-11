import base64
from app.utils.errors import BadRequestError

# 5 MB max (interview-friendly default)
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

# Allowed MIME types
ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}

# Magic numbers (file signatures)
MAGIC_NUMBERS = {
    "image/jpeg": [b"\xff\xd8\xff"],
    "image/png": [b"\x89PNG\r\n\x1a\n"],
    "image/gif": [b"GIF87a", b"GIF89a"],
    "image/webp": [b"RIFF"],  # WEBP starts with RIFF
}

def validate_image_upload(encoded_file: str, content_type: str) -> bytes:
    if not encoded_file:
        raise BadRequestError("Image file is required")

    # 1️⃣ MIME type validation
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise BadRequestError(
            f"Unsupported file type: {content_type}. Only image files are allowed."
        )

    # 2️⃣ Base64 decode validation
    try:
        decoded = base64.b64decode(encoded_file)
    except Exception:
        raise BadRequestError("Invalid base64 payload")

    # 3️⃣ File size enforcement
    if len(decoded) > MAX_FILE_SIZE_BYTES:
        raise BadRequestError(
            f"File size exceeds maximum allowed limit of {MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB"
        )

    # 4️⃣ Magic number (file signature) validation
    valid_signatures = MAGIC_NUMBERS.get(content_type, [])
    if not any(decoded.startswith(sig) for sig in valid_signatures):
        raise BadRequestError("File content does not match declared image type")

    return decoded
