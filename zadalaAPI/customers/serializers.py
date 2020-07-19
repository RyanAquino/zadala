from rest_framework import serializers
from customers.models import Customer
from suppliers.models import Supplier
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed



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


class CustomerLoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=65, write_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    first_name = serializers.CharField(max_length=255, read_only=True)
    last_name = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Customer
        fields = ['email', 'password', 'access', 'refresh', 'first_name', 'last_name']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        customer = auth.authenticate(email=email, password=password)

        if not customer:
            raise AuthenticationFailed('Invalid email/password')

        tokens = customer.tokens()

        return {
            'email': customer.email,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'access': tokens['token'],
            'refresh': tokens['refresh'],
        }
