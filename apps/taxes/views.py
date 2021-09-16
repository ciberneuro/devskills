from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Sum
from rest_framework import generics, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from . import serializers
from .models import Payable, Transaction


class PayableList(generics.ListAPIView):
    serializer_class = serializers.PendingPayableSerializer

    def get_queryset(self):
        if "service_type" in self.kwargs:
            self.serializer_class = serializers.PendingPayableFilteredSerializer
            service_type = self.kwargs["service_type"]
            return Payable.objects.filter(
                status=Payable.STATUS_PENDING, service_type=service_type
            )
        return Payable.objects.filter(status=Payable.STATUS_PENDING)


class TransactionsSummary(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        return Transaction.objects.none()

    def get(self, request, *args, **kwargs):
        date_start = self.kwargs["date_start"]
        date_end = self.kwargs["date_end"]
        transactions = (
            Transaction.objects.filter(pay_date__lte=date_end, pay_date__gte=date_start)
            .values("pay_date")
            .annotate(transactions=Count("pk"), amount = Sum("amount"))
        )
        transactions = [elem for elem in transactions]
        return Response(transactions)
