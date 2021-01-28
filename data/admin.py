from __future__ import unicode_literals

from django.contrib import admin
from .models import Data
from import_export.admin import ImportExportModelAdmin
from .resources import DataResource
# Register your models here.
@admin.register(Data)
class DataAdmin(ImportExportModelAdmin):
    resource_class = DataResource