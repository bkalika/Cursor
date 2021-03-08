from django.contrib import admin
from django.contrib.admin import register
from django.contrib.admin import ModelAdmin

from .models import Person, Room, Key, KeyTransfer, Tenant


@register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'phone')
    search_fields = ('first_name', 'last_name', 'phone', 'date_of_birth')
    list_filter = ('date_of_birth', 'last_name')


@register(Person)
class PersonAdmin(ModelAdmin):
    list_filter = ('id', 'name')
    search_fields = ('id', 'name')


@register(Room)
class RoomAdmin(ModelAdmin):
    list_display = ('number', 'owner', 'max_tenants')
    search_fields = ('number', 'owner', 'max_tenants')
    list_filter = ('owner', 'max_tenants')


@register(Key)
class KeyAdmin(ModelAdmin):
    search_fields = ('id', 'room')


@register(KeyTransfer)
class KeyTransferAdmin(ModelAdmin):
    list_display = ('key_out_data', 'key_in_data', 'room_id', 'person_id', 'guests', 'notes')
    search_fields = ('key_out_data', 'key_in_data', 'room_id', 'person_id', 'guests', 'notes')
    list_filter = ('key_out_data', 'key_in_data', 'room_id', 'person_id', 'guests', 'notes')
