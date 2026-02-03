"""
Models for Chemical Equipment Visualizer
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EquipmentDataset(models.Model):
    """Model to store uploaded equipment datasets"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(default=timezone.now)
    file_path = models.CharField(max_length=500)
    
    # Summary statistics
    total_equipment = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    
    class Meta:
        ordering = ['-upload_date']
        
    def __str__(self):
        return f"{self.filename} - {self.upload_date.strftime('%Y-%m-%d %H:%M')}"


class Equipment(models.Model):
    """Model to store individual equipment records"""
    
    dataset = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE, related_name='equipment')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return self.equipment_name
    
    class Meta:
        verbose_name_plural = "Equipment"
