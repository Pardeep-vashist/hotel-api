from django.urls import path
from .views import HotelRoomListView,IndexView

urlpatterns = [
    path('all_rooms/', HotelRoomListView.as_view(), name='hotel_room_list'),
]
