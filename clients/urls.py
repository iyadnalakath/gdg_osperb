from django.urls import path, include
from rest_framework_nested import routers
from . import views



router = routers.DefaultRouter()
router.register("client", views.ClientViewSet,basename="clients")
router.register("client-bank-account", views.ClientBankAccountViewSet,basename="client-bank-account")
router.register("bank-deposit-card", views.BankDepositCardViewSet,basename="client-bank-deposit-card")
# http://127.0.0.1:8000/gdg/clients/client-bank-account/?client={client id}    { api for listing client bank account according to client }

urlpatterns = [
    path('', include(router.urls)),
]


