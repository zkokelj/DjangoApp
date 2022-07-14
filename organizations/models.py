from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class Organization(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200)
    tax_number = models.CharField(
        max_length=8, validators=[RegexValidator(r"^[0-9]{8}$")]
    )
    mobile_number = models.CharField(
        max_length=13, validators=[RegexValidator(r"00|\+386[0-9]{8}")], null=True
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} - {self.tax_number}"


class OrganizationUser(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin"
        USER = "user"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(choices=Role.choices, max_length=5)

    def __str__(self):
        return f"{self.user} [ {self.organization} ] is {self.role}"
