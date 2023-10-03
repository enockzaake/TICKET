from django.urls import path
from django.conf.urls import handler404

from .import  views


urlpatterns = [
    path('',views.index,name='home'),
    path('events/',views.all_events_view,name='events'),
    path('event/details/<uuid:id>/',views.event_details,name='event-details'),
    path('events/buy-ticket/<uuid:id>/',views.buy_ticket,name='buy-ticket'), # merge with checkout url below
    path('create-event/',views.create_event,name='create-event'),
    path('event_admin/',views.event_admin,name='event_admin'),
    path('event_admin/edit-profile',views.editprofile,name='edit-profile'),
    path('event_admin/myTickets',views.myTickets,name='myTickets'),
    path('event_admin/edit-profile',views.editprofile,name='edit-profile'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.payment,name='payment'),
    path('callback/',views.callback_url,name='callback'),

    path('edit_event/<uuid:id>/',views.edit_event,name='edit_event')



]

handler404 = 'app.views.handler404'

 