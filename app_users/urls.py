from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path("account/", views.accountView, name="account"),
    path("login/", LoginView.as_view(template_name="app_users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", views.registrationView.as_view(), name="registration"),
]
