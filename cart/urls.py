from django.urls import path
from cart import views

urlpatterns = [
    path("add-to-cart/",views.AddToCart.as_view()),
    path("cart/", views.CartList.as_view()),
    path("cart-detail/<int:pk>/", views.CartDetail.as_view()),
    


]