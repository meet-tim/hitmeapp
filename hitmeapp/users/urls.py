from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="index"),

    path('products/<str:cat_filter>', views.products, name="products"),

    path('about/', views.about, name="about"),

    path('search/', views.search, name='search'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('add/', views.addProduct, name='create'),

    path('update/<int:product_id>', views.updateProduct, name="update"),

    #path('delete/<int:product_id>', views.deleteProduct, name="delete"),
    path('logout', views.logout_view,name="logout"),

    #ajax calls
    path('filterByAmount/<str:category>/<str:amount>', views.filterByAmount, name="filterByAmount"),

    path('filterByTime/<str:category>/<str:time>', views.filterByTime, name="filterByTime"),

    path('details/<int:product_id>', views.details, name="details"),

    path('delete/<int:product_id>', views.deleteProduct, name="delete"),

    path('suggestion/<str:msg>', views.suggestion, name="suggestion"),

]