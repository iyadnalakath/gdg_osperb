from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import serializers
from .models import User,PasswordRest
from .serializer import RegisterAdminSerializer,LoginSerializer,PasswordConfirmSerializer,PasswordResetSerializer,OTPConfirmationSerializer
from .permission import IsAdminUser


# Create your views here.


class RegisterAdminView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterAdminSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()

            data["email"] = user.email
            data["username"] = user.username
            data["pk"] = user.pk
            data["password"] = user.password
            data["last_login"] = user.last_login
            data["response"] = "successfully registered new user."
            

            token = Token.objects.get(user=user).key
            data["token"] = token

            status_code = status.HTTP_200_OK
            return Response(data, status=status_code)
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    
class AdminUserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]


    def get(self, request, pk=None):
        if pk:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = RegisterAdminSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            users = User.objects.all()
            serializer = RegisterAdminSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

class LoginView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        context = {}

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)

            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            context["response"] = "Successfully authenticated."
            context["pk"] = user.pk
            context["username"] = user.username.lower()
            context["token"] = token.key
            context["role"] = user.role
            context["last_login"] = user.last_login
            return Response(context, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            context["response"] = "Error"
            context["error_message"] = str(e.detail.get('non_field_errors')[0]) if 'non_field_errors' in e.detail else "Authentication failed"
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        context = {}
        try:
            request.user.auth_token.delete()
            context["response"] = "LogOut Successful."
            status_code = status.HTTP_200_OK
        except Exception as e:
            context["response"] = "Error"
            context["error_message"] = str(e)
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(context, status=status_code)
    

class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        
       
        response_data['otp_instance'] = str(response_data['otp_instance'])  
        return Response({'detail': 'OTP sent to your email.', 'otp_instance': response_data['otp_instance']})
    
class OTPConfirmationView(APIView):
    serializer_class = OTPConfirmationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:

            password_reset_instance = PasswordRest.objects.get(pk=serializer.validated_data['token'])
            password_reset_instance.is_active = True
            password_reset_instance.save()

            return Response({'detail': 'OTP confirmed successfully.'})
        except PasswordRest.DoesNotExist:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    
        
class PasswordConfirmView(APIView):
    serializer_class = PasswordConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password reset successfully.'})
    
