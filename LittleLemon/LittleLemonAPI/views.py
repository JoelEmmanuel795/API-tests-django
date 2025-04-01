from rest_framework import generics, status
from .models import MenuItem
from .serializers import MenuItemSerializer
from .serializers import MenuItemSerializerLess
from .serializers import MenuItemSerializerTaxed
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from rest_framework.response import Response
from rest_framework import viewsets
from .models import MenuItem
from .serializers import MenuItemSerializer  

# Create your views here.
class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializerTaxed

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializerTaxed

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
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__istartswith=search)
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)
        
        paginator = Paginator(items, per_page=perpage)
        try: 
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
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
