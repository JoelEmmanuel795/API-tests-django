from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def display_even_numbers(request):
    response = ''
    numbers = range(1, 10)
    for number in numbers:
        remainder = number % 2
        if remainder == 0:
            response += f'{number} is even<br>'
    
    return HttpResponse(response)