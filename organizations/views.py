from django.shortcuts import render

from django.http import HttpResponse

from organizations.models import Organization


def index(request):
    organizations = Organization.objects.order_by("-id")[:5]
    output = ", ".join([o.name for o in organizations])
    context = {"organizations": organizations}
    return render(request, "organizations/index.html", context)
