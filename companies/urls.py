from django.urls import path
from rest_framework_nested import routers
from .views import ActivityLogViewSet,CompanyBankAccountViewSet,SettingsViewSet


urlpatterns = [
    path('log/', ActivityLogViewSet.as_view(), name='activity-log'),
]

router = routers.DefaultRouter()
router.register("company-bank-account", CompanyBankAccountViewSet,basename="company-bank-account")
router.register("settings", SettingsViewSet,basename="settings")

urlpatterns = router.urls + urlpatterns