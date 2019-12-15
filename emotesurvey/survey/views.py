from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render


def index(request):
    return TemplateResponse(request, "index.html")


def survey(request):
    return render(request, "survey.html")


def thanks(request):
    return HttpResponse("<h2>Thanks!</h2>")
