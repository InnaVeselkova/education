from urllib.parse import urlparse
from rest_framework.exceptions import ValidationError


def validate_video_url(value):
    if value is None:
        return  # Ничего делать, если значение отсутствует

    if not isinstance(value, str):  # Убедитесь, что значение — строка
        raise ValidationError("Video URL must be a string.")

    parsed_url = urlparse(value)
    if not (parsed_url.scheme in ['http', 'https'] and
            (parsed_url.netloc.endswith("youtube.com") or parsed_url.netloc.endswith("youtu.be"))):
        raise ValidationError("Ссылка должна указывать только на видео youtube.com.")