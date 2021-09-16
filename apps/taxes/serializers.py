from .models import *
from rest_framework import serializers, viewsets


class PendingPayableSerializer(serializers.ModelSerializer):
    service_type = serializers.CharField(source="get_service_type_display")

    class Meta:
        model = Payable
        fields = [
            "service_type",
            "exp_date",
            "amount",
            "barcode",
        ]


class PendingPayableFilteredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payable
        fields = [
            "exp_date",
            "amount",
            "barcode",
        ]


class PayableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payable
        fields = [
            "url",
            "service_type",
            "description",
            "exp_date",
            "amount",
            "status",
            "barcode",
        ]


class PayableViewSet(viewsets.ModelViewSet):
    queryset = Payable.objects.all()
    serializer_class = PayableSerializer


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    barcode = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=Payable.objects
    )

    class Meta:
        model = Transaction
        fields = ["pk", "url", "method", "card_number", "pay_date", "barcode", "amount"]
    
    def validate(self, data):
        if data["method"] == Transaction.METHOD_CASH and data["card_number"] and data["card_number"] != "":
            raise serializers.ValidationError("Can't add a card number when paying with cash.")
        if data["method"] != Transaction.METHOD_CASH and not(data["card_number"] and data["card_number"] != ""):
            raise serializers.ValidationError("Card number required when not paying with cash.")
        if data["method"] != Transaction.METHOD_CASH and not luhn.is_valid(data["card_number"]):
            raise serializers.ValidationError("Card number is not valid.")
        return data


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
