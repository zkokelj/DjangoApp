from django.shortcuts import redirect, render

from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import Group

from django.http import HttpResponse
from organizations.forms import CreateUserForm

from organizations.models import Organization

from .decorators import unauthenticated_user, admin_only


@login_required(login_url="login")
def index(request):
    organization = (
        request.user.organizationuser.organization
        if hasattr(request.user, "organizationuser.organization")
        else None
    )
    context = {"organization": organization}
    return render(request, "organizations/index.html", context)


@login_required(login_url="login")
@admin_only
def edit(request):
    organizations = Organization.objects.order_by("-id")[:5]
    output = ", ".join([o.name for o in organizations])
    context = {"organizations": organizations}
    return render(request, "organizations/edit.html", context)


@login_required(login_url="login")
@admin_only
def editUsers(request):
    organizations = Organization.objects.order_by("-id")[:5]
    output = ", ".join([o.name for o in organizations])
    context = {"organizations": organizations}
    return render(request, "organizations/editusers.html", context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        print("In register POST...")
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            group = Group.objects.get(name="users")
            user.groups.add(group)

            messages.success(
                request,
                f"Account was created for: {username} ",
            )
            return redirect("login")

    context = {"form": form}
    return render(request, "organizations/register.html", context)


def userPage(request):
    content = {}
    return render(request, "account/user.html")


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Username or password is incorrect")

    context = {}
    return render(request, "organizations/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")
