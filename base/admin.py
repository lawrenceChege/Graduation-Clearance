from django.contrib import admin

# Register your models here.
from base.models import State


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    """
    State model admin. Defines the fields to display and which ones are searchable
    """
    list_filter = ('date_created',)
    list_display = ('name', 'description', 'date_modified', 'date_created')
    search_fields = ('name',)
