from django.shortcuts import render,redirect
from custom_auth.models import CustomUser as user 

import random
import string
import requests
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string   
from django.views.decorators.csrf import csrf_exempt


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
    return render(request,'index.html')

def create_event(request):
    if request.method == 'POST':
        name = request.POST['name']
        venue = request.POST['venue']
        start_datetime = request.POST['start_datetime']
        end_datetime = request.POST['end_datetime']
        event_banner = request.FILES.get('event_banner')
        event_description = request.POST['event_description']
        age_restriction = request.POST['age_restriction']
        
        
        event = Event.objects.create(
            name=name,
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
    # tickets = event.ticket_set.all() # to access tickets via reverse relationship
   
    return render(request,'event-details.html', {'event':event})
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

def modal(request):
    event = Event.objects.get(pk=1)
    # tickets = event.ticket_set.all() # to access tickets via reverse relationship
    return render(request,'flowmodal.html',{'event':event})

def event_admin(request):
    events = Event.objects.filter(event_organiser = request.user.id)
    return render(request,'admin.html',{'events':events})

@csrf_exempt
def checkout(request):
    return render(request,'checkout.html')

def handler404(request, exception):
    return render(request,'404.html')

@csrf_exempt
def callback_url(request):
    print("MPESA RESPONSE BODY:",request.POST)
    return  render(request,'404.html')

@csrf_exempt
def payment(request):
    # oauth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    # payload = ""
    # headers = {
    #     'Accept':'*/*',
    #     'Content-Type':'application/json',
    #     "Authorization":"Bearer "
    # }

    # response = requests.get(oauth_url, headers=headers)
    # print(response.text)
    print(request.POST)
    # telephone_number = request.POST.get('telephone_number')
    # print(telephone_number)
    return render(request,'404.html')

def editprofile(request):
    return render(request,'edit-profile.html')
    
def myTickets(request):
    return render(request,'edit-profile.html')
    