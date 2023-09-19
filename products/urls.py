from django.urls import path
from products import views

urlpatterns = [
    path("products/<int:pk>",views.ProductDetail.as_view()),
    path("products/", views.ProductsListCreate.as_view()),
    # path("products/price-descending/", views.SortDescPrice.as_view()),    #based on the most expensive
    # path("products/price-ascending/", views.SortAscPrice.as_view()),    #based on cheapest
    path("chart/<int:prod_id>", views.ChartList.as_view()),
    # path("search-product/price-descending/", views.SearchTitleDesc.as_view()),
    # path("search-product/price-ascending/", views.SearchTitleAsc.as_view()),

]