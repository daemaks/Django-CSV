from django.contrib.auth.models import User
from django.db import models


class DataSchema(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Column(models.Model):
    TYPES = (
        ("full_name", "Full Name"),
        ("job", "Job"),
        ("email", "Email"),
        ("domain_name", "Domain Name"),
        ("phone_number", "Phone Number"),
        ("company_name", "Company Name"),
        ("text", "Text"),
        ("integer", "Integer"),
        ("address", "Address"),
        ("date", "Date"),
    )

    schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPES)
    order = models.IntegerField()

    # extra arguments for some types
    range_start = models.IntegerField(blank=True, null=True)
    range_end = models.IntegerField(blank=True, null=True)
    sentences = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name
