from rest_framework import serializers
from suppliers.models import Supplier
from customers.models import Customer

class SupplierSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8)
    email = serializers.EmailField(max_length=255, min_length=4)
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = Supplier
        fields = '__all__'

    def validate(self, attrs):
        email = attrs.get('email', '')

        if Supplier.objects.filter(email=email).exists() or Customer.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already in use'})
        return super().validate(attrs)

    def create(self, validated_data):
        return Supplier.objects.create_user(**validated_data)
