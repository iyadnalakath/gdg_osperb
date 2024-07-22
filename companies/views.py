from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly,IsAuthenticated
from .models import ActivityLog,CompanyBankAccount,Settings
from .serializer import ActivityLogSerializer,CompanyBankAccountSerializer,SettingsSerializer



class ActivityLogViewSet(generics.ListCreateAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]

class CompanyBankAccountViewSet(ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin"]:
            queryset = CompanyBankAccount.objects.all()
            serializer = CompanyBankAccountSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to view Company bank account.")
        
    def retrieve(self, request, *args, **kwargs):
        try:
            company_bank_account = self.get_object()
            if request.user.role in ["admin"]:
                serializer = CompanyBankAccountSerializer(company_bank_account)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to view this object.")
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except CompanyBankAccount.DoesNotExist:
            return Response({'error': 'Company bank account not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request, *args, **kwargs):
        try:
            serializer = CompanyBankAccountSerializer(data=request.data)
            if serializer.is_valid():
                if self.request.user.role == "admin":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    raise PermissionDenied("You are not allowed to create this object.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        company_bank_account = self.get_object()
        try:
            if request.user.role == "admin":
                company_bank_account.delete()
                return Response({'response': 'Company bank account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except CompanyBankAccount.DoesNotExist:
            return Response({'error': 'Company bank account not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            company_bank_account = self.get_object()
            serializer = CompanyBankAccountSerializer(company_bank_account, data=request.data, partial=True)
            if serializer.is_valid():
                if request.user.role == "admin":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied("You are not allowed to update this object.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except CompanyBankAccount.DoesNotExist:
            return Response({'error': 'Company bank account not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SettingsViewSet(ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin"]:
            queryset = Settings.objects.all()
            serializer = SettingsSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to view Settings.")
        
    def retrieve(self, request, *args, **kwargs):
        try:
            settings = self.get_object()
            if request.user.role in ["admin"]:
                serializer = SettingsSerializer(settings)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to view this object.")
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except CompanyBankAccount.DoesNotExist:
            return Response({'error': 'Settings not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request, *args, **kwargs):
        try:
            serializer = SettingsSerializer(data=request.data)
            if serializer.is_valid():
                if self.request.user.role == "admin":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    raise PermissionDenied("You are not allowed to create this object.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        settings = self.get_object()
        try:
            if request.user.role == "admin":
                settings.delete()
                return Response({'response': 'settings deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Settings.DoesNotExist:
            return Response({'error': 'settings not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            settings = self.get_object()
            serializer = SettingsSerializer(settings, data=request.data, partial=True)
            if serializer.is_valid():
                if request.user.role == "admin":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied("You are not allowed to update this object.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Settings.DoesNotExist:
            return Response({'error': 'settings not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)