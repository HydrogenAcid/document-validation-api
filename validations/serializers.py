#Validacion de entrada 
from rest_framework import serializers
from .models import Validation

class ValidationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validation
        fields = ['id', "title", "status", "created_at"]
        read_only_fields = ['id', "status", "created_at"]

class ValidationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validation
        fields = [
            'id', "title", "status", 
            "extracted_key", "extracted_value",
            "created_at"
            ]
        
