from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import LedgerHead,Ledger,LedgerEntry
from .serializer import LedgerHeadSerializer,LedgerSerializer,LedgerEntrySerializer
# Create your views here.


class LedgerHeadViewSet(ModelViewSet):
    queryset = LedgerHead.objects.all()
    serializer_class = LedgerHeadSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin"]:
            queryset = LedgerHead.objects.all()
            serializer = LedgerHeadSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to view ledger head.")
        
    def retrieve(self, request, *args, **kwargs):
        try:
            ledger_head = self.get_object()
            if request.user.role in ["admin"]:
                serializer = LedgerHeadSerializer(ledger_head)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to view this object.")
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except LedgerHead.DoesNotExist:
            return Response({'error': 'ledger head not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request, *args, **kwargs):
        try:
            serializer = LedgerHeadSerializer(data=request.data)
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
        ledger_head = self.get_object()
        try:
            if request.user.role == "admin":
                ledger_head.delete()
                return Response({'response': 'ledger head deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except LedgerHead.DoesNotExist:
            return Response({'error': 'ledger head not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            ledger_head = self.get_object()
            serializer = LedgerHeadSerializer(ledger_head, data=request.data, partial=True)
            if serializer.is_valid():
                if request.user.role == "admin":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied("You are not allowed to update this object.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except LedgerHead.DoesNotExist:
            return Response({'error': 'ledger head not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LedgerViewSet(ModelViewSet):
    queryset = Ledger.objects.all()
    serializer_class = LedgerSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin"]:
            queryset = Ledger.objects.all()
            serializer = LedgerSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to view ledger.")
        
    def retrieve(self, request, *args, **kwargs):
        try:
            ledger = self.get_object()
            if request.user.role in ["admin"]:
                serializer = LedgerSerializer(ledger)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to view this object.")
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Ledger.DoesNotExist:
            return Response({'error': 'ledger not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request, *args, **kwargs):
        try:
            serializer = LedgerSerializer(data=request.data)
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
        ledger = self.get_object()
        try:
            if request.user.role == "admin":
                ledger.delete()
                return Response({'response': 'ledger deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except LedgerHead.DoesNotExist:
            return Response({'error': 'ledger not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            ledger = self.get_object()
            serializer = LedgerSerializer(ledger, data=request.data, partial=True)
            if serializer.is_valid():
                if request.user.role == "admin":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied("You are not allowed to update this object.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Ledger.DoesNotExist:
            return Response({'error': 'ledger not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LedgerEntryViewSet(ModelViewSet):
    queryset = LedgerEntry.objects.all()
    serializer_class = LedgerEntrySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin"]:
            queryset = LedgerEntry.objects.all()
            serializer = LedgerEntrySerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to view ledger entry.")
        
    def retrieve(self, request, *args, **kwargs):
        try:
            ledger_entry = self.get_object()
            if request.user.role in ["admin"]:
                serializer = LedgerEntrySerializer(ledger_entry)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to view this object.")
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except LedgerEntry.DoesNotExist:
            return Response({'error': 'ledger_entry not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request, *args, **kwargs):
        try:
            serializer = LedgerEntrySerializer(data=request.data)
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
        ledger_entry = self.get_object()
        try:
            if request.user.role == "admin":
                ledger_entry.delete()
                return Response({'response': 'ledger deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except LedgerHead.DoesNotExist:
            return Response({'error': 'ledger not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            ledger_entry = self.get_object()
            serializer = LedgerEntrySerializer(ledger_entry, data=request.data, partial=True)
            if serializer.is_valid():
                if request.user.role == "admin":
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied("You are not allowed to update this object.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except LedgerEntry.DoesNotExist:
            return Response({'error': 'ledger_entry not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
