from rest_framework import serializers
from .models import UserData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = [
            "id",
            "email",
            "name",
            "password",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
        ]

    def create(self, validated_data):
        user = UserData.objects.create(
            email=validated_data["email"],
            name=validated_data["name"],
            is_staff=validated_data.get("is_staff", False),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ["email", "name"]
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = [
            "id",
            "email",
            "name",
            "password"]
    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.name = validated_data.get("name", instance.name)
        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
