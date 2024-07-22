from django.urls import path
from rest_framework_nested import routers
from .views import TransferViewSet


urlpatterns = [
    
]

router = routers.DefaultRouter()
router.register("transfer", TransferViewSet,basename="transfers")

urlpatterns = router.urls + urlpatterns