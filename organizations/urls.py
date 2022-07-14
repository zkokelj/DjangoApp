from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("", views.index, name="index"),
    path("edit/", views.edit, name="edit"),
    path("editusers/", views.editUsers, name="edit-users"),
    path("orgpdf/", views.organizationPDF, name="org-pdf"),
    path("orgjson/", views.organizationJSON, name="org-json"),
    path("adduser/<int:id>", views.addUser, name="add-user"),
    path("removeuser/<int:id>", views.removeUser, name="remove-user"),
]
