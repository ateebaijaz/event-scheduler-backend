# views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h2>Go to <a href='/swagger/'>Swagger</a> for EVENT MANAGEMENT SYSTEM APIs</h2>")
