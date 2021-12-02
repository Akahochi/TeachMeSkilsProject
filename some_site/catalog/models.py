import os.path
import uuid

from django.db import models

from catalog.validators import validate_resolution, MIN_PRODUCT_HEIGHT, MIN_PRODUCT_WIDTH


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='Наименование')
    description = models.TextField(max_length=256, verbose_name='Описание')
    slug = models.SlugField(max_length=32, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


def get_file_path(instance, image_name):
    ext = image_name.split('.')[-1]
    new_name = f'{uuid.uuid4()}.{ext}'
    return os.path.join('products', new_name)


class Product(models.Model):
    name = models.CharField(max_length=32, verbose_name='Наименование')
    description = models.TextField(max_length=256, verbose_name='Описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    vegan_or_not = models.BooleanField(verbose_name='Vegeterian?')
    slug = models.SlugField(max_length=32, unique=True)

    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    modifier_groups = models.ManyToManyField("ModifierGroup", blank=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name='Изображения',
        upload_to=get_file_path,
        null=True, blank=True,
        validators=[validate_resolution],
        help_text=f'Минимальное разрешение - {MIN_PRODUCT_HEIGHT}x{MIN_PRODUCT_WIDTH} '
    )

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'Изображение для {self.product.name}'


class ModifierGroup(models.Model):
    name = models.CharField(max_length=32, verbose_name='Наименование')
    discription = models.TextField(max_length=256, verbose_name='Описание')
    slug = models.SlugField(max_length=32, unique=True)

    class Meta:
        verbose_name = 'Группа модификаторов'
        verbose_name_plural = 'Группы модификаторов'

    def __str__(self):
        return self.name


class Modifier(models.Model):
    name = models.CharField(max_length=32, verbose_name='Наименование')
    description = models.TextField(max_length=256, blank=True, null=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    vegan_or_not = models.BooleanField(verbose_name='Vegeterian?')
    slug = models.SlugField(max_length=32, unique=True)
    modifier_group = models.ForeignKey(
        "ModifierGroup",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Группа модификаторов'
    )

    class Meta:
        verbose_name = 'Модификатор'
        verbose_name_plural = 'Модификаторы'

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    name = models.CharField(max_length=32, verbose_name='Наименование характеристики')

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return self.name


class ProductSpecificationValue(models.Model):
    specification = models.ForeignKey('ProductSpecification', on_delete=models.CASCADE)
    value = models.CharField(max_length=400, verbose_name='Значение характеристики')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Значение характеристики'
        verbose_name_plural = 'Значения характеристик'

    def __str__(self):
        return f'{self.specification.name} - {self.value}'
