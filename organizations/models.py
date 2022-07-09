from django.db import models
from django.core.validators import RegexValidator


class Organizations(models.Model):
    name = models.CharField(max_length=200)
    # TODO: :ASK: Should address have multiple fileds (street, city, country)?
    address = models.CharField(max_length=200)
    tax_number = models.CharField(
        max_length=8, validators=[RegexValidator(r"^[0-9]{8}$")]
    )
