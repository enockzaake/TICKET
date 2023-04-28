from django.shortcuts import render,redirect

import random
import string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.conf import settings
import uuid


from .models import Event,Ticket
from django.conf import settings

def generate_ticket_number():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
#  add bar code


# dispaly the random ticket to user 
# def index(request):
#     if request.method == 'POST':
#         ticket = generate_ticket_number()
#         return render(request,'index.html',{'ticket':ticket})
#     return render(request,'index.html')

def index(request):
    print(settings.BASE_DIR)
    return render(request,'web3.html')

def create_event(request):
    if request.method == 'POST':
        name = request.POST['name']
        venue = request.POST['venue']
        age_restriction = request.POST['age_restriction']
        date = request.POST['date']
        event = Event.objects.create(name=name,venue=venue , age_restriction = age_restriction,date=date)
        event.save()
        # add validation for the incoming POST data
        ticket_name = request.POST['ticket_name']
        ticket_type = request.POST['ticket_type']
        ticket_price = request.POST['ticket_price']
        ticket_quantity = request.POST['ticket_quantity']
        ticket = Ticket.objects.create(name = ticket_name,event=event,ticket_type=ticket_type,price=ticket_price,quantity_available=ticket_quantity)
        ticket.save()
        event.save()
        return redirect('/events/')
    return render(request,'create-event.html')

def all_events_view(request):
    # query = request.GET.get('query')
    query = request.POST.get('query')
    if query:
        events = Event.objects.filter(name__icontains=query)
        return render(request,'events2.html',{'events':events,'query':query})
    events = Event.objects.all()
    return render(request,'all-events.html',{'events':events})

def event_details(request,id):
    event = Event.objects.get(pk=id)
    tickets = event.ticket_set.all() # to access tickets via reverse relationship
    print("TICKETS:",tickets)
    return render(request,'event-details.html',{'event':event,'tickets':tickets})
# join these two views into get and post [post for sending confirmation email]

def buy_ticket(request,id):
    #add form for user to enter email and phone number (also add option for use current details if logged in )
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        ticket = generate_ticket_number()
        subject = 'TICKET CONFIRMATION FOR ' + event.name.upper() 
        message = 'Thank you. Your ticket number is ' + ticket
        from_email = settings.EMAIL_HOST_USER
        # recipient_list = ['zaakeenock@gmail.com']
        # send_mail(subject, message, from_email, recipient_list)
        html_message = render_to_string('emailtemplate.html')
        plain_message = strip_tags(html_message)
        from_email = from_email
        recipient_list = ['zaakeenock@gmail.com']
        
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

        return render(request,'email-confirmation.html')
    return render(request,'buy-ticket.html',{'events':event})
