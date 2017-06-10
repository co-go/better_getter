from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("<h1> Item could not be found! </h1>")

def get_item_details(request, item_name):
    context = { "item_name": item_name }
    return render(request, 'get_item/item.html', context)
