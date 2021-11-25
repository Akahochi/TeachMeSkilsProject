from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile

MIN_PRODUCT_WIDTH = 400
MIN_PRODUCT_HEIGHT = 400

def validate_resolution(image: ImageFieldFile):
    if image.width < MIN_PRODUCT_WIDTH or image.height < MIN_PRODUCT_HEIGHT:
        raise ValidationError(
            f'Разрешение изображения должно быть не '
            f'менее {MIN_PRODUCT_WIDTH}x{MIN_PRODUCT_HEIGHT}'
        )