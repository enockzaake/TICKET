from django.db import models
from custom_auth.models import CustomUser
from datetime import datetime
import uuid

# events related models
class Venue(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    seating_capacity = models.IntegerField()

    def __str__(self):
        return self.name  

class Event(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    event_organiser = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)  # the logged in user creating the account 
    organiser_name = models.CharField(max_length=256,default='ORGANISER') # name to display on the events page
    name = models.CharField(max_length=255)
    start_datetime = models.DateTimeField(blank=True,null=True)
    end_datetime = models.DateTimeField(blank=True,null=True)
    venue = models.CharField(max_length=255)        # enter event name or ad option to choose from map
    event_banners = models.ImageField(blank=True,null=True ,upload_to='media/')
    event_description = models.TextField(blank=True,null=True)
    age_restriction = models.CharField(max_length=10,blank=True,null=True)
    active = True
    # website = models.URLField(default="")
    # twitter = models.URLField(default="")
    # instagram = models.URLField(default="")
    # facebook = models.URLField(default="")

    def __str__(self):
        return self.name
     
class Ticket(models.Model):
    TICKET_TYPES = ( ('PAID','PAID'),('FREE','FREE'),('DONATIONS','DONATIONS') )
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=50)
    event = models.ForeignKey(Event,null=True,blank=True , on_delete=models.CASCADE,related_name='tickets')
    ticket_type = models.CharField(max_length=255,choices=TICKET_TYPES)  
    price = models.DecimalField(decimal_places=2, max_digits=8)
    quantity_available = models.IntegerField()   # change to number of tickets to be i.e one may buy many tickets of the same type

    quantity_bought = models.IntegerField(default=0,editable=False)  # Track the number of tickets bought

    def __str__(self):
        return self.name + " ticket for " + self.event.name 

class UserTicket(models.Model):
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=20, unique=True)

# to show on organiser dashboard   
class Transaction(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE) # change to use reverse relationship
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    transaction_datetime = models.DateTimeField(auto_now_add=True)
                                                                                                                                                