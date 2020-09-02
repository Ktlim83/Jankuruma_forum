from django.shortcuts import render, redirect , HttpResponse
from log_reg_app.models import *
from .models import *
from django.contrib import messages
import os
# THIS IMPORT IS FOR FILE UPLOADS
from django.core.files.storage import FileSystemStorage

# Create your views here.

def map_dashboard(request):
    # if check checks if there is a user logged in, if not it redirects
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            "map_api" : os.environ.get('GMAP2_APIKEY'),
            
        }
        return render (request, 'map_dashboard.html', context)
    
def junkyard(request):
    # if check checks if there is a user logged in, if not it redirects
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            "map_api" : os.environ.get('GMAP2_APIKEY'),
            
        }
        return render (request, 'junkyard.html', context)
    
    
    