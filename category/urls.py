from django.urls import path
from category import views

urlpatterns = [
    path("category/", views.CategoryDetail.as_view()),

]