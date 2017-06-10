from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1> get_item Homepage </h1>")
