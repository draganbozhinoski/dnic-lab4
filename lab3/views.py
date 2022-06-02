from django.shortcuts import render
from .models import BlogPost


# Create your views here.

def index(request):
    listaBlogovi = BlogPost.objects.all()
    context = {"blogs": listaBlogovi}
    return render(request, 'index.html', context=context)
