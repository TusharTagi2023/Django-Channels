from django.shortcuts import render,redirect
from .models import Group,Chats
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.http import JsonResponse

# Create your views here.
def index(request, grpname=None):
    if request.method == 'GET':
        group=Group.objects.filter(gpname=grpname).first()
        chats=[]
        if group:
            chats=Chats.objects.filter(group=group)
        else:
            group=Group.objects.create(gpname=grpname).save
        return render(request, 'Home.html',{'data':grpname,"chats":chats})
    
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(f'/group/{grpname}')
        else:
            return JsonResponse({"error":"Password or username is incorrect"})
