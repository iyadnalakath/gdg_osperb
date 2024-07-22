from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Transfer
from .serializer import TransferSerializer

# Create your views here.


class TransferViewSet(ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin"]:
            queryset = Transfer.objects.all()
            serializer = TransferSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to view Transfer.")
        
    def retrieve(self, request, *args, **kwargs):
        try:
            transfer = self.get_object()
            if request.user.role in ["admin"]:
                serializer = TransferSerializer(transfer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to view this object.")
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Transfer.DoesNotExist:
            return Response({'error': 'Transfer not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request, *args, **kwargs):
        try:
            serializer = TransferSerializer(data=request.data)
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
        transfer = self.get_object()
        try:
            if request.user.role == "admin":
                transfer.delete()
                return Response({'response': 'Transfer deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Transfer.DoesNotExist:
            return Response({'error': 'transfer not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            transfer = self.get_object()
            serializer = TransferSerializer(transfer, data=request.data, partial=True)
            if serializer.is_valid():
                if request.user.role == "admin":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied("You are not allowed to update this object.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Transfer.DoesNotExist:
            return Response({'error': 'transfer not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)