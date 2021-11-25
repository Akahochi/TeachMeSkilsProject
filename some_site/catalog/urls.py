from django.urls import path, include

from . import views
from .views import HomeViev, ProductView

app_name = 'catalog'

urlpatterns = [
    path('', HomeViev.as_view(), name='home'),
    path('category/<slug:category_slug>/', views.category_view, name='category'),
    path('product/<slug:product_slug>/', ProductView.as_view(), name='product'),

]
