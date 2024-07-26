from django.urls import path
from rest_framework_nested import routers
from .views import TransferViewSet,DepositViewSet


urlpatterns = [
    
]

router = routers.DefaultRouter()
router.register("transfer", TransferViewSet,basename="transfers")
router.register("deposit", DepositViewSet,basename="deposits")

urlpatterns = router.urls + urlpatterns