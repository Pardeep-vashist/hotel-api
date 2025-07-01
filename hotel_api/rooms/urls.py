# rooms/urls.py

from django.urls import path
from .views import HotelRoomListView, check_availability
from . import views

urlpatterns = [
    path('all_rooms/', HotelRoomListView.as_view(), name='hotel_room_list'),
    path('api/check-availability/', check_availability, name='check_availability'),
    path('book-room/', views.book_room_view, name='book-room'),
    path('confirm-booking/', views.confirm_booking_view, name='confirm-booking'),
    path('api/add-room', views.check_roomtype_availability, name='add_room'),
]
