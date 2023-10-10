# django
from django.db import models

# Order model that is used to create a table in a database.
class Order(models.Model):
    ORDER_STATUS = (
        ('STATUS_BOOK',         'B'),
        ('STATUS_TICKET',       'T'),
        ('STATUS_VOID',         'V'),
        ('STATUS_REFUND',       'R'),
        ('STATUS_BOOK_ERROR',   'E'),
        ('STATUS_TICKET_ERROR', 'C'),
        ('STATUS_PAID_WAIT',    'O'),
        ('STATUS_IN_PROGRESS',  'G'),
        ('STATUS_VOID_ERROR',   'W'),
        ('STATUS_REFUND_ERROR', 'F'),
    )
    
    order_number      = models.BigIntegerField(primary_key=True)
    gds_pnr           = models.CharField(max_length=255)
    supplier_pnr      = models.CharField(max_length=255)
    status            = models.CharField(max_length=255, choices=ORDER_STATUS, default='STATUS_BOOK')
    created_at        = models.DateTimeField(auto_now_add=False)
    ticket_time_limit = models.DateTimeField(null=True, blank=True)
    void_time_limit   = models.IntegerField(null=True, blank=True)
    price_info        = models.JSONField()
    currency          = models.CharField(max_length=255)
    fare              = models.JSONField()
    provider          = models.JSONField()

    class Meta:
        ordering = ['-order_number']

# Agent model that is used to create a table in a database.
# It is related to Order model.
class Agent(models.Model):
    order      = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="agent")
    agent_id   = models.UUIDField()
    agent_name = models.CharField(max_length=300)

# Passenger model that is used to create a table in a database.
# It is related to Order model.
class Passenger(models.Model):
    PASSENGER_CATEGORIES = (
        ('ADT', 'ADT'),
        ('CHD', 'CHD'),
        ('INF', 'INF'),
        ('INS', 'INS')
    )

    PASSENGER_TYPES = (
        ('Citizen',   'Citizen'),
        ('Student',   'Student'),
        ('Disabled',  'Disabled'),
        ('Pensioner', 'Pensioner'),
    )

    GENDER_TYPES = (
        ('Male',   'Male'),
        ('Female', 'Female')
    )

    order              = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='passengers')
    passenger_id       = models.UUIDField(primary_key=True)
    firstname          = models.CharField(max_length=255)
    lastname           = models.CharField(max_length=255)
    middlename         = models.CharField(max_length=255)
    gender             = models.CharField(choices=GENDER_TYPES)
    birth_date         = models.DateField()
    passenger_category = models.CharField(choices=PASSENGER_CATEGORIES)
    passenger_type     = models.CharField(choices=PASSENGER_TYPES)
    phone_number       = models.CharField(max_length=255)
    email_address      = models.CharField(max_length=255)

# Ticket model that is used to create a table in a database.
# It is related to Passenger model.
class Ticket(models.Model):
    passenger    = models.OneToOneField(Passenger, on_delete=models.CASCADE, related_name='ticket_info')
    price_info   = models.JSONField()
    fares_info   = models.JSONField()
    baggage_info = models.JSONField()

# Document model that is used to create a table in a database.
# It is related to Passenger model.
class Document(models.Model):
    passenger       = models.OneToOneField(Passenger, on_delete=models.CASCADE, related_name='document')
    passport_number = models.CharField(max_length=255)
    passport_expiry = models.DateField()
    citizenship     = models.CharField(max_length=255)
    document_type   = models.CharField(max_length=300)
