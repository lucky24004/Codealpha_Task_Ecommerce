from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("login/", views.user_login, name="login"),   # ✅ custom login
    path("logout/", views.user_logout, name="logout"), # ✅ custom logout
    path("signup/", views.signup_view, name="signup"),
    path("cart/", views.cart_view, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("add-to-cart/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
