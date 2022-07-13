from django.shortcuts import redirect, render

from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import Group

from organizations.forms import CreateUserForm

from organizations.models import Organization

from .decorators import unauthenticated_user, admin_only

from django.http import FileResponse, HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4


@login_required(login_url="login")
def organizationPDF(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 16)

    lines = [
        "Organization report:",
        "",
    ]

    try:
        organization = request.user.organizationuser.organization
        lines.append(f"Name: {organization.name}")
        lines.append(f"Address: {organization.address}")
        lines.append(f"Tax number: {organization.tax_number}")
        lines.append(f"Mobile number: {organization.mobile_number}")
    except:
        return HttpResponse("You are not part of any organization yet.")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="organization.pdf")


@login_required(login_url="login")
def organizationJSON():
    pass


@login_required(login_url="login")
def index(request):
    try:
        organization = request.user.organizationuser.organization
    except:
        organization = None

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
