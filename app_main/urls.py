from django.urls import path
from .views import (
    product_list,
    category_list,
    category_products,
    product_detail,
    cart_view,
    add_to_cart,
    remove_from_cart,
    update_cart_item,
    checkout,search
)

urlpatterns = [
    path('search/', search, name='search'),
    path("", product_list, name="product"),
    path("categories/", category_list, name="category-list"),
    path("category/<int:category_id>/", category_products, name="category_products"),
    path("product/<int:pk>/", product_detail, name="product_detail"),
    
    path("cart/", cart_view, name="cart"),  # Savatni ko'rsatish
    path("add_to_cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path(
        "remove_from_cart/<int:product_id>/", remove_from_cart, name="remove_from_cart"
    ),
    path('update_cart_item/<int:product_id>/', update_cart_item, name='update_cart_item'),

    path('checkout/', checkout, name='checkout'),
    
]
