from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import Group

from organizations.forms import CreateUserForm, EditOrganization

from organizations.models import Organization, OrganizationUser

from .decorators import unauthenticated_user, admin_only

from django.http import FileResponse, HttpResponse, JsonResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4


@login_required(login_url="login")
@admin_only
def addUser(request, id):
    user = get_object_or_404(User, id=id)
    added = OrganizationUser(
        user=user, organization=request.user.organizationuser.organization, role="user"
    )
    added.save()
    return redirect("edit-users")


@login_required(login_url="login")
@admin_only
def removeUser(request, id):
    user = get_object_or_404(User, id=id)
    try:
        if (
            user.organizationuser.organization
            == request.user.organizationuser.organization
        ):
            instance = OrganizationUser.objects.get(user=user)
            instance.delete()
            return redirect("edit-users")
        else:
            return HttpResponse(
                "Forbidden  to remove users that are not part of your org."
            )
    except:
        return HttpResponse("Forbidden!")


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
def organizationJSON(request):
    response = {}
    try:
        organization = request.user.organizationuser.organization
        response["name"] = organization.name
        response["address"] = organization.address
        response["tax_number"] = organization.tax_number
        response["mobile_number"] = organization.mobile_number
        return JsonResponse(response)

    except:
        return HttpResponse("You are not part of any organization yet.")


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
    if request.method == "POST":
        print(f"Request method POST + {request.POST}")

        try:
            org = request.user.organizationuser.organization
        except:
            return HttpResponse("User doesn't belong to an instance")

        form = EditOrganization(
            request.POST, instance=org, initial={"name": "abc", "address": "def"}
        )
        if form.is_valid():
            form.save()
            return redirect("edit")
        else:
            print(form.errors.as_data())
            return render(request, "organizations/edit.html", {"form": form})

    return render(request, "organizations/edit.html", {"form": EditOrganization})


@login_required(login_url="login")
@admin_only
def editUsers(request):
    usersorg = list(OrganizationUser.objects.values_list("user", flat=True))
    users = User.objects.exclude(id__in=usersorg)

    org = request.user.organizationuser.organization
    sameorgusers = (
        OrganizationUser.objects.filter(organization=org)
        .filter(role="user")
        .values_list("user", flat=True)
    )
    myusers = User.objects.filter(id__in=sameorgusers)

    context = {"users": users, "myusers": myusers}
    return render(request, "organizations/editusers.html", context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
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
