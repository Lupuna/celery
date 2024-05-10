from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'products', views.ProductsView, basename='products')

urlpatterns = [
    path('', include(router.urls))
]