from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

def loadmain(request):
    return render(request, 'apptpage.html')

