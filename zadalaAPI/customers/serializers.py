from rest_framework import serializers
from customers.models import Customer
from suppliers.models import Supplier


class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8)
    email = serializers.EmailField(max_length=255, min_length=4)
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = Customer
        fields = '__all__'

    def validate(self, attrs):
        email = attrs.get('email', '')

        if Customer.objects.filter(email=email).exists() or Supplier.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already in use'})
        return super().validate(attrs)

    def create(self, validated_data):
        return Customer.objects.create_user(**validated_data)
