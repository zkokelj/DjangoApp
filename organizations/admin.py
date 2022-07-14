from django.contrib import admin

from .models import Organization, OrganizationUser
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Organization, SimpleHistoryAdmin)
admin.site.register(OrganizationUser)
