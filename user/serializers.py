from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .utils.otp import get_stored_otp, clear_stored_otp, generate_otp, store_otp
from .utils.email_notifiers import send_otp_email

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
            raise serializers.ValidationError(_("Username or email is already in use."))

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
            raise serializers.ValidationError(_("Invalid username/email."))

        if not user.check_password(password):
            raise serializers.ValidationError(_("Incorrect Password."))

        data['user'] = user
        return data


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'email', 'is_online', 'last_online', )

    def update(self, instance, validated_data):
        for attr, val in validated_data.items():
            setattr(instance, attr, val)

        instance.save()
        return instance


class PasswordChangeOTPGenerationSerializer(serializers.Serializer):
    def create(self, data):
        user = self.context["request"].user

        otp = generate_otp(user.id)
        store_otp(user.id, otp)

        # print(f"✨✨✨SENDING THE EMAIL...")
        send_otp_email(to_email=str(user.email), otp=otp)
        # print(f"✨✨✨email: {user.email} otp: {otp}")
        return data


class PasswordChangeOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context["request"].user
        stored_otp = get_stored_otp(user.id)

        if not stored_otp:
            raise serializers.ValidationError(_("OTP has expired or is invalid."))
        if data["otp"] != stored_otp:
            raise serializers.ValidationError(_("Invalid OTP. Please generate a new OTP."))

        validate_password(data["new_password"], user)
        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()

        clear_stored_otp(user.id)
        return user


#IMP
#rate limitter figure out
#pass change api
#redis dashboard look do
#figure out what else can be done here - celery and stuff
