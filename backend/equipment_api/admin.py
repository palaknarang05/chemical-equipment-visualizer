"""
Admin configuration for Equipment API
"""
from django.contrib import admin
from .models import EquipmentDataset, Equipment


@admin.register(EquipmentDataset)
class EquipmentDatasetAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'upload_date', 'total_equipment']
    list_filter = ['upload_date', 'user']
    search_fields = ['filename', 'user__username']
    readonly_fields = ['upload_date']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['equipment_type', 'dataset']
    search_fields = ['equipment_name', 'equipment_type']
