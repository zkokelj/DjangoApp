from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=200)
    # TODO: :ASK: Should address have multiple fileds (street, city, country)?
    address = models.CharField(max_length=200)
    tax_number = models.CharField(
        max_length=8, validators=[RegexValidator(r"^[0-9]{8}$")]
    )

    def __str__(self):
        return f"{self.name} - {self.tax_number}"


class OrganizationAdmin(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
