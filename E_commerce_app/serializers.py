from rest_framework import serializers
from .models import category_list,categories

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model=categories
        fields='__all__'


class category_list_serializer(serializers.ModelSerializer):
    
    class Meta:
        model=category_list
        fields='__all__'



