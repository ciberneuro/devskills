from django.urls import path, include, re_path
from rest_framework import routers
from . import views
from . import serializers

router = routers.DefaultRouter()
router.register(r"payables", serializers.PayableViewSet)
router.register(r"transactions", serializers.TransactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    re_path("^pending_payables/(?P<service_type>.+)/$", views.PayableList.as_view()),
    re_path("^pending_payables/$", views.PayableList.as_view()),
    re_path(
        "^transaction_summary/(?P<date_start>.+)/(?P<date_end>.+)/$",
        views.TransactionsSummary.as_view(),
    ),
]
