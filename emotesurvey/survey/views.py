from django.shortcuts import render


def survey(request):
    return render(request, "survey.html")
