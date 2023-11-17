from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signupView, name="Sign Up"),
    path('login/', views.loginView, name="Login"),
    path('logout/', views.logoutView, name="Logout")
]
