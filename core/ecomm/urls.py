from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name="home"),
    path('Products', views.products, name="products"),
    path('product/<int:id>/', views.productView, name="product"),
    path('profile/', views.profileView, name="profile"),
    path('cart/', views.cartView, name="cart"),
    path('checkout/', views.checkoutView, name="checkout"),
    path('thankyou/', views.thankyouView, name="thankyou"),
    path('orders/', views.orderView, name="orders"),
]
