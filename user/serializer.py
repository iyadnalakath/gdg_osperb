import string
import random
from uuid import UUID
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User,PasswordRest
from .functions import send_otp_email

class RegisterAdminSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Enter confirm password",
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["id","username", "email", "country", "password", "password2", "last_login"]

        read_only_fields = ("password2", "id", "last_login")


    def create(self, validated_data):
        password = self.validated_data["password"]


        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        else:
            user = User.objects.create(
                username=validated_data["username"],
                email=validated_data["email"]
            ) 

            user.set_password(validated_data["password"])
            user.raw_password = validated_data["password"]
            user.role = "admin"
            user.is_admin = True
            user.save()
            return user
        


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Incorrect username")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")

        return user
    
class LogoutSerializer(serializers.Serializer):
    pass



      
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email address.")
        return value

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        
        otp = ''.join(random.choices(string.digits, k=4))
        
       
        password_reset_instance = PasswordRest.objects.create(user=user, otp=otp)
        print(otp)
        
      
        send_otp_email(user.email, otp)

        return {'otp_instance': password_reset_instance.id, 'parent_serializer_context': self.context}
        
class OTPConfirmationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=4)
    token = serializers.CharField()

    def validate(self, data):
      
        try:
            password_reset_instance = PasswordRest.objects.get(pk=data['token'], is_active=True)
            if password_reset_instance.otp != data['otp']:
                raise serializers.ValidationError("Invalid OTP.")
        except PasswordRest.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")
        
        return data

    
class PasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)
    token = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self):
        try:
            token_uuid = UUID(str(self.validated_data['token']))
            print(f"Token UUID: {token_uuid}")
            user = PasswordRest.objects.get(pk=token_uuid, is_active=True).user
            user.password = make_password(self.validated_data['password'])
            user.save()

        except PasswordRest.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired token.")
        except Exception as e:
            raise serializers.ValidationError(f"An error occurred: {str(e)}")