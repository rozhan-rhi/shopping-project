from django.urls import path
from products import views

urlpatterns = [
    path("products/<int:pk>",views.ProductDetail.as_view()),
    path("products/", views.ProductsListCreate.as_view())

]