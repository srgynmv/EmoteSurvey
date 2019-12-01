from django.http import HttpResponse
from django.template.response import TemplateResponse


def index(request):
    return TemplateResponse(request, "index.html")

def about(request):
    return HttpResponse("<h2>About</h2>")


def contact(request):
    return HttpResponse("<h2>Contacts</h2>")