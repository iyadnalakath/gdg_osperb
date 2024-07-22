from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import BankDepositCard,ClientBankAccount,Client
from .serializer import ClientSerializer,ClientListSerializer,ClientBankAccountSerializer,BankDepositCardSerializer

# Create your views here.


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            if request.user.role in ["admin"]:
                clients = Client.objects.all()
                clients_count = Client.objects.count()

                serializer = ClientListSerializer({
                    'clients_count': clients_count,
                    'clients': clients
                })
                return Response(serializer.data)
            else:
                raise PermissionDenied("You are not allowed to view clients.")
        except Client.DoesNotExist:
            return Response({'error': 'Clients not found.'}, status=404)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=403)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    def retrieve(self, request, *args, **kwargs):
        try:
            client = self.get_object()
            if request.user.role in ["admin"]:
                serializer = ClientSerializer(client)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to view this object.")
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request, *args, **kwargs):
        try:
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                if self.request.user.role == "admin":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    raise PermissionDenied("You are not allowed to create this object.")
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        clinet = self.get_object()
        try:
            if request.user.role == "admin":
                clinet.delete()
                return Response({'response': 'client deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Client.DoesNotExist:
            return Response({'error': 'client not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            client = self.get_object()
            serializer = ClientSerializer(client, data=request.data, partial=True)
            if serializer.is_valid():
                if request.user.role == "admin":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied("You are not allowed to update this object.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClientBankAccountViewSet(ModelViewSet):
    serializer_class = ClientBankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ClientBankAccount.objects.all()
        client_id = self.request.query_params.get('client', None)
        
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin"]:
            queryset = self.get_queryset()
            serializer = ClientBankAccountSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to view client bank accounts.")

        
    def retrieve(self, request, *args, **kwargs):
        try:
            client_bank_account = self.get_object()
            if request.user.role in ["admin"]:
                serializer = ClientBankAccountSerializer(client_bank_account)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to view this object.")
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ClientBankAccount.DoesNotExist:
            return Response({'error': 'client bank account not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request, *args, **kwargs):
        try:
            serializer = ClientBankAccountSerializer(data=request.data)
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
        bank_account = self.get_object()
        try:
            if request.user.role == "admin":
                bank_account.delete()
                return Response({'response': 'client bank account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ClientBankAccount.DoesNotExist:
            return Response({'error': 'client bank account not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            bank_account = self.get_object()
            serializer = ClientBankAccountSerializer(bank_account, data=request.data, partial=True)
            if serializer.is_valid():
                if request.user.role == "admin":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied("You are not allowed to update this object.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Client.DoesNotExist:
            return Response({'error': 'Client bank account not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BankDepositCardViewSet(ModelViewSet):
    queryset = BankDepositCard.objects.all()
    serializer_class = BankDepositCardSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin"]:
            queryset = BankDepositCard.objects.all()
            serializer = BankDepositCardSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to view client bank deposit card.")
        
    def retrieve(self, request, *args, **kwargs):
        try:
            bank_deposit_card = self.get_object()
            if request.user.role in ["admin"]:
                serializer = BankDepositCardSerializer(bank_deposit_card)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to view this object.")
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except BankDepositCard.DoesNotExist:
            return Response({'error': 'bank deposit card not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request, *args, **kwargs):
        try:
            serializer = BankDepositCardSerializer(data=request.data)
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
        bank_deposit_card = self.get_object()
        try:
            if request.user.role == "admin":
                bank_deposit_card.delete()
                return Response({'response': 'bank deposit card deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except BankDepositCard.DoesNotExist:
            return Response({'error': 'bank deposit card not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            bank_deposit_card = self.get_object()
            serializer = BankDepositCardSerializer(bank_deposit_card, data=request.data, partial=True)
            if serializer.is_valid():
                if request.user.role == "admin":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied("You are not allowed to update this object.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except BankDepositCard.DoesNotExist:
            return Response({'error': 'Bank deposit card not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
