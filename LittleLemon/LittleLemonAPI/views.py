from rest_framework import generics, status
from .models import MenuItem
from .serializers import MenuItemSerializer
from .serializers import MenuItemSerializerLess
from .serializers import MenuItemSerializerTaxed
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
    serialized_item = MenuItemSerializer(items, many=True)
    return Response(serialized_item.data)

@api_view()
def get_single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializerLess(item)
    return Response(serialized_item.data)

@api_view(['GET', 'POST'])
def get_taxed_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        serialized_item = MenuItemSerializerTaxed(items, many=True)
        return Response(serialized_item.data)
    if request.method == 'POST': 
        serialized_item = MenuItemSerializerTaxed(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)

@api_view()
def get_categories(request):
    from .models import Category
    from rest_framework import serializers

    class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = '__all__'

    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
