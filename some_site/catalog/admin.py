from django.contrib import admin
from . import models


class ProductImageInline(admin.StackedInline):
    model = models.ProductImage
    max_num = 3
    extra = 0


class ProductSpecificationValueInline(admin.TabularInline):
    model = models.ProductSpecificationValue
    max_num = 15
    extra = 0


@admin.register(models.ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    inlines = [ProductImageInline, ProductSpecificationValueInline]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.ModifierGroup)
class ModifierGroupAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Modifier)
class ModifierAdmin(admin.ModelAdmin):
    list_display = ['name', 'modifier_group']
