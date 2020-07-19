from django.contrib.auth.backends import BaseBackend
from rest_framework import serializers
from suppliers.models import Supplier
from customers.models import Customer
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed


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


class SupplierAuth(BaseBackend):
    def authenticate(self, request=None, **credentials):

        try:
            user = Supplier.objects.get(email=request['email'])
            password = check_password(password=request['password'], encoded=user.password)
        except Supplier.DoesNotExist:
            return 'Account does not exist'

        if password:
            return user
        return False


class SupplierLoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=65, write_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    first_name = serializers.CharField(max_length=255, read_only=True)
    last_name = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Supplier
        fields = ['email', 'password', 'access', 'refresh', 'first_name', 'last_name']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        auth = SupplierAuth()

        supplier = auth.authenticate(request={'email': email, 'password': password})

        if supplier == 'Account does not exist' or not supplier:
            raise AuthenticationFailed('Invalid email/password')

        tokens = supplier.tokens(supplier)

        return {
            'email': supplier.email,
            'first_name': supplier.first_name,
            'last_name': supplier.last_name,
            'access': tokens['token'],
            'refresh': tokens['refresh'],
        }
        # return super().validate(attrs)

