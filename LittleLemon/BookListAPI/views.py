from django.shortcuts import render
from rest_framework.response import Response
# from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET', 'POST'])
def books(request):
    return Response('list of the books', status=status.HTTP_200_OK)

# def books(request):
#     return HttpResponse('list of the books', status=status.HTTP_200_OK)