"""
Serializers for Chemical Equipment Visualizer API
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EquipmentDataset, Equipment


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for Equipment model"""
    
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class EquipmentDatasetSerializer(serializers.ModelSerializer):
    """Serializer for EquipmentDataset model"""
    
    equipment = EquipmentSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = EquipmentDataset
        fields = ['id', 'filename', 'upload_date', 'total_equipment', 
                  'avg_flowrate', 'avg_pressure', 'avg_temperature', 
                  'equipment', 'username']


class DatasetSummarySerializer(serializers.ModelSerializer):
    """Serializer for dataset summary (without full equipment list)"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = EquipmentDataset
        fields = ['id', 'filename', 'upload_date', 'total_equipment', 
                  'avg_flowrate', 'avg_pressure', 'avg_temperature', 'username']
