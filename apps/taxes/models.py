from django.db import models
from datetime import date
from cardvalidator import luhn
import uuid

# Elaborado en base a los requerimientos
# Tipo de servicio (Luz/Gas/etc...)
# Descripción del servicio. Ej: 'Edenor S.A.'
# Fecha de vencimiento. Ej (2021-01-15)
# Importe del servicio.
# Status del pago (pending, paid, etc.).
# Código de barra (debe ser único - PK)


class Payable(models.Model):
    SERVICE_ELECTRIC = "electric"
    SERVICE_GAS = "gas"
    SERVICE_WATER = "water"
    SERVICE_INTERNET = "internet"
    SERVICE_OTHERS = "others"
    SERVICES = (
        (SERVICE_ELECTRIC, "Electric"),
        (SERVICE_GAS, "Gas"),
        (SERVICE_WATER, "Water"),
        (SERVICE_INTERNET, "Internet"),
        (SERVICE_OTHERS, "Others"),
    )
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_CANCELLED = "cancelled"
    STATUS = (
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_CANCELLED, "Cancelled"),
    )
    service_type = models.CharField(max_length=100, choices=SERVICES)
    description = models.CharField(max_length=500)
    exp_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=STATUS, default=STATUS_PENDING)
    barcode = models.BigIntegerField(primary_key=True)


# Elaborado en base a los requerimientos
# Método de pago (debit_card, credit_card o cash)
# Número de la tarjeta (solo en caso de no ser efectivo)
# Importe del pago
# Código de barra
# Fecha de pago


class Transaction(models.Model):
    METHOD_DEBIT = "debit"
    METHOD_CREDIT = "credit"
    METHOD_CASH = "cash"
    METHODS = (
        (METHOD_DEBIT, "Debit Card"),
        (METHOD_CREDIT, "Credit Card"),
        (METHOD_CASH, "Cash"),
    )
    method = models.CharField(max_length=100, choices=METHODS)
    card_number = models.CharField(max_length=200, blank=True)
    pay_date = models.DateField(default=date.today)
    barcode = models.ForeignKey(Payable, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.method == self.METHOD_CASH and self.card_number and self.card_number != "":
            raise ValueError("Can't add a card number when paying with cash.")
        if self.method != self.METHOD_CASH and not(self.card_number and self.card_number != ""):
            raise ValueError("Card number required when not paying with cash.")
        if self.method != self.METHOD_CASH and not luhn.is_valid(self.card_number):
            raise ValueError("Card number is not valid.")
        super().save(*args, **kwargs)
        payable = self.barcode
        payable.status = Payable.STATUS_PAID
        payable.save()

