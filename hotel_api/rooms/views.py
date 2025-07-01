from django.shortcuts import render,  get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RoomType
from .serializers import RoomTypeSerializer
from rest_framework.decorators import api_view
from datetime import datetime
from booking.models import Booking
from django.http import JsonResponse
from rooms.models import RoomType
from django.db.models import Q, Count, Sum


# Hotel Room List View
class HotelRoomListView(APIView):                                                                                                                                             
    def get(self, request):
        hotel_id = request.GET.get('hotel_id')
        if not hotel_id:
            return Response({"error": "hotel_id is required"}, status=400)
        
        rooms = RoomType.objects.filter(hotel_id=hotel_id)
        serializer = RoomTypeSerializer(rooms, many=True)
        return Response(serializer.data)
    
def book_room_view(request):
    room_id = request.GET.get('room_id')
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    room = get_object_or_404(RoomType, id=room_id)

    context = {
        'room': room,
        'check_in': check_in,
        'check_out': check_out,
    }
    return render(request, 'book_room.html', context)

def confirm_booking_view(request):
    # For now, just render a confirmation page
    return render(request, 'confirm_booking.html')


# Check Availability View
@api_view(['GET'])
def check_availability(request):
    check_in_str = request.GET.get('check_in')
    check_out_str = request.GET.get('check_out')

    if not check_in_str or not check_out_str:
        return JsonResponse({'error': 'check_in and check_out are required.'}, status=400)

    try:
        check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    # Step 1: Get bookings that overlap with the given date range
    overlapping_bookings = Booking.objects.filter(
        Q(check_in__lt=check_out) & Q(check_out__gt=check_in)
    )

    # Step 2: Sum number_of_rooms per room type
    booked_counts = (
        overlapping_bookings
        .values('category_id')
        .annotate(booked_count=Sum('no_of_room'))
    )
    booked_dict = {item['category_id']: item['booked_count'] or 0 for item in booked_counts}

    # Step 3: Get all room types that have total_rooms > 0
    all_rooms = RoomType.objects.filter(total_rooms__gt=0)

    # Step 4: Filter out room types that are fully booked
    available_rooms = []
    for room in all_rooms:
        booked = booked_dict.get(room.id, 0)
        available_count = room.total_rooms - booked
        if available_count > 0:
            available_rooms.append({
                'id': room.id,
                'name': room.name,
                'description': room.description,
                'price_per_night': str(room.price_per_night),
                'available_rooms': available_count,
                'image': [img.image.url for img in room.image.all()] if room.image.exists() else [],
            })

    return JsonResponse(available_rooms, safe=False)

@api_view(['GET'])
def check_roomtype_availability(request):
    check_in_str = request.GET.get('check_in')
    check_out_str = request.GET.get('check_out')
    room_type_id = request.GET.get('room_type_id')

    if not all([check_in_str, check_out_str, room_type_id]):
        return JsonResponse({'error': 'check_in, check_out, and room_type_id are required.'}, status=400)

    try:
        check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    if check_in >= check_out:
        return JsonResponse({'error': 'check_out must be after check_in.'}, status=400)

    try:
        room_type = RoomType.objects.get(id=room_type_id)
    except RoomType.DoesNotExist:
        return JsonResponse({'error': 'Room type not found.'}, status=404)

    # Get number of rooms already booked in this room type
    overlapping_bookings = Booking.objects.filter(
        Q(check_in__lt=check_out) & Q(check_out__gt=check_in),
        category_id=room_type_id
    ).aggregate(booked_count=Sum('no_of_room'))

    booked_count = overlapping_bookings['booked_count'] or 0
    available_rooms = room_type.total_rooms - booked_count

    return JsonResponse({
        'room_type_id': room_type.id,
        'room_type_name': room_type.name,
        'total_rooms': room_type.total_rooms,
        'available_rooms': available_rooms,
        'is_available': available_rooms > 0
    })