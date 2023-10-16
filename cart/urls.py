from django.urls import path
from cart import views

urlpatterns = [
    path("add-to-cart/",views.AddToCart.as_view()),
    path("cart/", views.ShowCart.as_view()),


]