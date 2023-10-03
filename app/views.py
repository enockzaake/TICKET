from django.shortcuts import render,redirect
from custom_auth.models import CustomUser as user 

import random
import string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string   
from django.views.decorators.csrf import csrf_exempt

from .models import Event,Ticket
from django.conf import settings
from django.http import JsonResponse
from django.http import QueryDict
from django.core.serializers import serialize
import json
import uuid

def generate_ticket_number():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def index(request):
    test_id = uuid.uuid4()
    return render(request,'index.html',{'id':test_id})

def create_event(request):
    if request.method == 'POST':
        event_name = request.POST['name']
        organiser_name = request.POST['organiser_name']
        venue = request.POST['venue']
        start_datetime = request.POST['start_datetime']
        end_datetime = request.POST['end_datetime']
        event_banner = request.FILES.get('event_banner')
        event_description = request.POST['event_description']
        age_restriction = request.POST['age_restriction']
        website = request.POST.get('website_url',None)
        twitter = request.POST.get('twitter_url',None)
        instagram = request.POST.get('instagram_url',None)
        facebook = request.POST.get('facebook_url',None)
        
        
        event = Event.objects.create(
            event_organiser = request.user,
            organiser_name = organiser_name,
            name=event_name,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            venue=venue,
            event_banners = event_banner,
            age_restriction = age_restriction,
            event_description = event_description
            )
        
        event.save()
        paid_tickets = request.POST.getlist('paid')
        paid_tickets_price = request.POST.getlist('paidprice')
        paid_tickets_quantity = request.POST.getlist('paidquantity')
        free_tickets = request.POST.getlist('free') 
        free_tickets_price = request.POST.getlist('freeprice')
        free_tickets_quantity = request.POST.getlist('freequantity')
        donations_tickets = request.POST.getlist('donations')
        donations_tickets_price = request.POST.getlist('donationsprice')
        donations_tickets_quantity = request.POST.getlist('donationsquantity')

        if len(paid_tickets) > 0 :
            for i,name in enumerate(paid_tickets):
                ticket = Ticket.objects.create(name = name ,event=event,ticket_type='PAID',price=paid_tickets_price[i],quantity_available=paid_tickets_quantity[i])
                ticket.save()
        if len(free_tickets) > 0 :
            for i,name in enumerate(free_tickets):
                ticket = Ticket.objects.create(name = name ,event=event,ticket_type='FREE',price=free_tickets_price[i],quantity_available=free_tickets_quantity[i])
                ticket.save()
        if len(donations_tickets) > 0 :
            for i,name in enumerate(donations_tickets):
                ticket = Ticket.objects.create(name = name ,event=event,ticket_type='DONATIONS',price=donations_tickets_price[i],quantity_available=donations_tickets_quantity[i])
                ticket.save()
                
        event.save()
 
        return redirect('/events/')  #change to redirect to dashboard
    return render(request,'maintickets.html')

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
    tickets = event.tickets.all() # to access tickets via reverse relationship
   
    return render(request,'event-details.html', {'event':event,'tickets':tickets})
# join these two views into get and post [post for sending confirmation email]
    
def buy_ticket(request,id):
    event = None
    #add form for user to enter email and phone number (also add option for use current details if logged in )
    if request.method == 'POST':
        
        event = Event.objects.get(id=1)
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


def event_admin (request):
    events = Event.objects.filter(event_organiser = request.user)

    event_data = []

    for event in events:
        tickets = event.tickets.all()
        total_ticket_quantity = sum(ticket.quantity_bought for ticket in tickets)

        event_data.append(
            {
                'event':event,
                'total_ticket_quantity':total_ticket_quantity
            }
        )

    return render(request,'admin.html',{'event_data':event_data})

@csrf_exempt
def checkout(request):

    return render(request,'checkout.html')

@csrf_exempt
def payment(request):

    phone_number = request.POST['telephone_number']
    email = request.POST['email']
    payment_method = request.POST['payment_method']

    event_data = json.loads(request.POST['json_data'])

    ticket_uuid_strings = event_data["ticket_ids"]  # for reference when looping

    # check if incoming price is same as in database and if number of incoming tickets * price is equal to that given
    # amount_to_checkevent_data = ["order_summary"]["total_amount"] / event_data["order_summary"]["ticket_quantity"]
    print(event_data)
    for ticket_id in event_data["order_summary"]:
        if ticket_id.startswith("ticket-"):
            id = uuid.UUID(ticket_uuid_strings[ticket_id])
            ticket = Ticket.objects.get(pk=id)
            ticket.quantity_bought += int(event_data["order_summary"][ticket_id])
            ticket.save()

    # if payment_method == "mobile-money":
    #     "MPESA"(phone_number,event_data["order_summary"]["total_amount"])

    event_id = uuid.UUID(event_data["event_id"])
    event = Event.objects.get(pk=event_id)


    return render(request,'404.html')

def handler404(request, exception):
    return render(request,'404.html')

@csrf_exempt
def callback_url(request):
    print("MPESA RESPONSE BODY:",request.POST)
    return  render(request,'testdetails.html')


def editprofile(request):
    return render(request,'edit-profile.html')
    
def myTickets(request):
    return render(request,'edit-profile.html')
    

def edit_event(request,id):
    if request.method == 'GET':
        try:
            # Add redis cache to limit queries being made for same resource
            event = Event.objects.get(pk=id)
            event_json = serialize('json',[event])
            return JsonResponse({'event':json.loads(event_json)[0]})
        except Event.DoesNotExist:
            return JsonResponse({'Error':'Event not found'})
    else:
        try:
            event = Event.objects.get(pk=1)
            event.name = request.POST['name']
            event.venue = request.POST['venue']
            event.start_datetime = request.POST['start_datetime']
            event.end_datetime = request.POST['end_datetime']
            # event.event_banner = request.FILES.get('event_banner')
            event.event_description = request.POST['event_description']
            event.age_restriction = request.POST['age_restriction']
            event.save()
            
        except Event.DoesNotExist:
            return JsonResponse({'Error':'Event not found'})
        return render(request,'index.html')


