from django.contrib import admin

from .models import Venue,Event,Ticket,Transaction
# Register your models here.
admin.site.register(Event)
# admin.site.register(Venue)
admin.site.register(Ticket)
admin.site.register(Transaction)
