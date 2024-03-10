from django.shortcuts import render, redirect


# Create your views here.
def mainpage(request):
    return render(request, 'main/index.html')


