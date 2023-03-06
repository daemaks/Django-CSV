from django.contrib import admin
from .models import Column, DataSchema

admin.site.register((Column, DataSchema))
