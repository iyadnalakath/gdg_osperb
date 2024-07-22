from django.urls import path, include
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register("ledger-head", views.LedgerHeadViewSet,basename="ledger-head")
router.register("ledger", views.LedgerViewSet,basename="ledger")
router.register("ledger_entry", views.LedgerEntryViewSet,basename="ledger_entry")

urlpatterns = [
    path('', include(router.urls)),
]

