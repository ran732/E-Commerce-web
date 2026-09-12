from django.urls import path
from store import views

urlpatterns = [
    path('',views.store, name="store"),
    path('catogery/<slug:category_slug>/',views.store,name='products_by_category'),
    path('catogery/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
]
