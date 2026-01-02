from django.shortcuts import render
from django.http import HttpResponse
from .models import Record


def index(request):
    return HttpResponse(Record.objects.all())
