# Desafio Back-end
Este código responde al desafío técnico propuesto en https://github.com/newcombin/devskillsback

## Instalación

El código fue implementado con python 3.9.6 con los siguientes paquetes:
```
django
djangorestframework
markdown
django-filter
Card-Validator
```

Las versiones de los paquetes y sus dependencias se encuentran en el archivo requirements.txt. Una forma directa de instalarlos es creando un entorno virtual. Por ejemplo:
```
python3 -m venv env-devskills
. env-devskills/bin/activate
pip install -r requirements.txt
```
Después se deben cargar las migraciones, crear un usuario y levantar el servidor.
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Endpoints

El enunciado menciona endpoints, los cuales seran listados a continuación, mas la ruta de la implementación
<br/>
<br/>

### 1.
>Debe permitir crear una boleta de pago son la siguiente información, recibiendo la siguiente información:
>    * Tipo de servicio (Luz/Gas/etc...)
>    * Descripción del servicio. Ej: `'Edenor S.A.'`
>    * Fecha de vencimiento. Ej (2021-01-15)
>    * Importe del servicio.
>    * Status del pago (pending, paid, etc.).
>    * Código de barra (debe ser único - PK)

Listado: http://localhost:8000/taxes/payables/
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "url": "http://localhost:8000/taxes/payables/3/",
            "service_type": "water",
            "description": "Water Inc",
            "exp_date": "2021-09-30",
            "amount": "1000.00",
            "status": "pending",
            "barcode": 3
        },
        {
            "url": "http://localhost:8000/taxes/payables/4/",
            "service_type": "water",
            "description": "Water Inc",
            "exp_date": "2021-09-30",
            "amount": "2000.00",
            "status": "pending",
            "barcode": 4
        }
    ]
}
```
CRUD: http://localhost:8000/taxes/payables/&lt;barcode&gt;/<br/>
Mediante los métodos HTTP: `GET, PUT, PATCH, DELETE`
<br/>
<br/>

### 2.
>Debe permitir realizar un pago (transacción), recibiendo la siguiente información:
>    * Método de pago (`debit_card`, `credit_card` o `cash`)
>    * Número de la tarjeta (solo en caso de no ser efectivo)
>    * Importe del pago
>    * Código de barra
>    * Fecha de pago

Listado: http://localhost:8000/taxes/transactions/
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "pk": 6,
            "url": "http://localhost:8000/taxes/transactions/6/",
            "method": "debit",
            "card_number": "123455",
            "pay_date": "2021-09-15",
            "barcode": 1,
            "amount": "1500.00"
        },
        {
            "pk": 7,
            "url": "http://localhost:8000/taxes/transactions/7/",
            "method": "cash",
            "card_number": "",
            "pay_date": "2021-09-15",
            "barcode": 2,
            "amount": "2500.00"
        }
    ]
}
```
CRUD: http://localhost:8000/taxes/transactions/`pk`/<br/>
Mediante los métodos HTTP: `GET, PUT, PATCH, DELETE`
<br/>
<br/>

### 3.
>Debe permitir listar aquellas boletas impagas en forma total o filtradas por tipo de servicio, devolviendo la siguiente información:
>    * Tipo de servicio (solo si se lista sin filtro)
>    * Fecha de vencimiento
>    * Importe del servicio
>    * Código de barra

http://localhost:8000/taxes/pending_payables/<br/>
http://localhost:8000/taxes/pending_payables/water/<br/>
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "exp_date": "2021-09-30",
            "amount": "1000.00",
            "barcode": 3
        },
        {
            "exp_date": "2021-09-30",
            "amount": "2000.00",
            "barcode": 4
        }
    ]
}
```
<br/>
<br/>

### 4.
>Debe permitir listar los pagos (transacciones) entre un período de fechas, acumulando por día, devolviendo la siguiente información:
>    * Fecha de pago
>    * Importe acumulado
>    * Cantidad de transacciones en esa fecha

http://localhost:8000/taxes/transaction_summary/`date_start`/`date_end`/<br/>
```
[
    {"pay_date":"2021-09-15","transactions":2,"amount":4000.0},
    {"pay_date":"2021-09-16","transactions":2,"amount":4000.0}
]
```

## Supuestos

1. Este es un código de demo y por lo tanto no posee una configuración de producción.
2. Los documentos no están asociados a los usuarios. Todo usuario con permiso puede crear facturas o borrar facturas y pagar facturas creadas por otros usuarios.
3. Registrar un pago cambia el estado de la boleta de pendiente a pagado. No se revierte el estado a pendiente ya que esto implica verificar múltiples condiciones fuera del alcance de la demo (anulación, eliminación, cambio de código de barra). 
4. Si bien los casos fuera del alcance mencionado en el punto anterior deberían estar bloqueados. Se han dejado habilitados por flexibilidad considerando que es una demo.
