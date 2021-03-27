from rest_framework import serializers
from .models import Quote, Role, Show
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import User

class QuoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Quote
		fields = ("quote", 'role', "show")
	role = serializers.CharField(source="role.name")
    show = serializers.CharField(source="show.name")

class AdminAddUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("id","username", "first_name", 'last_name', "email", "password2", "password1", "is_superuser", "is_active", "is_staff")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True}
        }

    def validate(self, attrs):
        if self.context['request'].user.username != "faran":
            raise serializers.ValidationError({"detail": "you dont have permission to perform this action", "hint": "contact user 'faran'"})
        if attrs['password2'] != attrs["password1"]:
            raise serializers.ValidationError({"password": "password fields dont match"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=validated_data['is_active'],
            is_superuser=validated_data['is_superuser']
        )
        user.set_password(validated_data["password1"])
        user.save()
        return user


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ("name", "slug")
        read_only_fields = ("slug", )

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("name", "slug")
        read_only_fields = ("slug", )


class AdminQuoteSerializer(serializers.ModelSerializer):
    role = serializers.CharField(required=True)
    show = serializers.CharField(required=True)
    class Meta:
        model = Quote
        fields = ("key", "quote", "role", "show")

    def create(self, validated_data):
        role_name = validated_data.get("role").title()
        show_name = validated_data.get("show").title()
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            role = Role.objects.create(name=role_name)
        try:
            show = Show.objects.get(name=show_name)
        except Show.DoesNotExist:
            show = Show.objects.create(name=show_name)
        quote = Quote.objects.create(
            quote=validated_data['quote'],
            show=show,
            role=role
        )
        return quote
