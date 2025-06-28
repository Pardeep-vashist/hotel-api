from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RoomType
from .serializers import RoomTypeSerializer

# Create your views here.

class HotelRoomListView(APIView):                                                                                                                                             
    def get(self, request):
        hotel_id = request.GET.get('hotel_id')
        if not hotel_id:
            return Response({"error": "hotel_id is required"}, status=400)
        
        rooms = RoomType.objects.filter(hotel_id=hotel_id)
        serializer = RoomTypeSerializer(rooms, many=True)
        return Response(serializer.data)