from django.urls import path
from .views import HotelIndexView

urlpatterns = [
    path('<str:hotel_name>',HotelIndexView.as_view()),
]
