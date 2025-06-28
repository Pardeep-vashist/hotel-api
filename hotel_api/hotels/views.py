from django.shortcuts import render,get_object_or_404
from django.views import View
from django.http import Http404
from .models import Hotel
# Create your views here.

class HotelIndexView(View):
    def get(self,request,*args,**kwargs):
        hotel = get_object_or_404(Hotel,name=kwargs['hotel_name'])
        return render(request,'index.html',{'hotel':hotel})                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    

