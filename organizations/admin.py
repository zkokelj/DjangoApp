from django.contrib import admin

from .models import Organization, OrganizationAdmin

admin.site.register(Organization)
admin.site.register(OrganizationAdmin)
