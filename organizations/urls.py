from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("", views.index, name="index"),
    path("user/", views.userPage, name="user-page"),
    path("edit/", views.edit, name="edit"),
]
