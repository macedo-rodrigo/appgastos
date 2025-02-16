from rest_framework import serializers
from .models import Gasto, Ahorro, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'  # Serializa todos los campos

class GastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasto
        fields = '__all__'

class AhorroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ahorro
        fields = '__all__'