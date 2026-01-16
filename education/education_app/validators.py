from django.core.exceptions import ValidationError
from urllib.parse import urlparse

def validate_video_url(value):
    if value:
        parsed_url = urlparse(value)
        if not parsed_url.netloc.endswith("youtube.com") and not parsed_url.netloc.endswith("youtu.be"):
            raise ValidationError("Ссылка должна указывать только на видео youtube.com")