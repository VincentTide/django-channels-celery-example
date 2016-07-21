from django.shortcuts import render, get_object_or_404
from .models import Job


def index(request):
    return render(request, 'jobs/index.html')
