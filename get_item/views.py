from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1> Item could not be found! </h1>")

def get_item_details(request, item_name):
    return HttpResponse("Page for the item: " + item_name)
