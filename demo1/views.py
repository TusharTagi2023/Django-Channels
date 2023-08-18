from django.shortcuts import render

# Create your views here.
def index(request, grpname):
    return render(request, 'Home.html',{'data':grpname})