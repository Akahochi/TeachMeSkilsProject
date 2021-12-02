import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def get_file_path(instance, image_name):
    ext = image_name.split('.')[-1]
    new_name = f'{uuid.uuid4()}.{ext}'
    return os.path.join('products', new_name)


class User(AbstractUser):
    avatar = models.ImageField(
        verbose_name='Avatar',
        upload_to=get_file_path,
        blank=True,
        null=True
    )
    email = models.EmailField(verbose_name='email', unique=True)
