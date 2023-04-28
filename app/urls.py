from django.urls import path

from .import  views


urlpatterns = [
    path('',views.index,name='home'),
    path('create-event/',views.create_event,name='create-event'),
    path('events/',views.all_events_view,name='events'),
    path('events/details/<id>/',views.event_details,name='event-details'),
    path('events/buy-ticket/<id>/',views.buy_ticket,name='buy-ticket'), # check out

]
 