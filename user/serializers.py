from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")

        is_exists = User.objects.filter(Q(username = username) | Q(email = email)).exists()
        if is_exists:
            raise serializers.ValidationError("Username or email is already in use.")

        return data

    def create(self, validated_data):
        return User.objects.create_user(
            username = validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"]
        )



class LoginUserSerializer(serializers.ModelSerializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["password", "identifier"]

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        user = User.objects.filter(Q(email = identifier) | Q(username = identifier)).first()

        if user is None:
            raise serializers.ValidationError("Invalid username/email.")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect Password.")

        data['user'] = user
        return data



