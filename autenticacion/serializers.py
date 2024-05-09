from rest_framework import serializers
from .models import UserData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password", "is_staff", "is_active", "date_joined", "last_login"]

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'],
                                       name=validated_data['name'],
                                       is_staff=validated_data['is_staff']
                                       )
        user.set_password(validated_data['password'])
        user.save()
        return user
