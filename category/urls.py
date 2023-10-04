from django.urls import path
from category import views

urlpatterns = [
    path("category/<int:pk>/", views.CategoryDetail.as_view()),
    path("categories/", views.CategoryList.as_view()),
    path("subcategory/<int:pk>/", views.SubCategoryDetail.as_view()),
    path("subcategories/", views.SubCategoryList.as_view()),

]