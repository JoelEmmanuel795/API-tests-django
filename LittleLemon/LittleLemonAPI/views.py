from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from .serializers import MenuItemSerializerLess
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

@api_view()
def get_menu_items(request):
    items = MenuItem.objects.all()
    serialized_item = MenuItemSerializerLess(items, many=True)
    return Response(serialized_item.data)

@api_view()
def get_single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializerLess(item)
    return Response(serialized_item.data)