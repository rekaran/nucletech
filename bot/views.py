from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'bot/index.html')


def realestate(request):
    return render(request, 'bot/realestate.html')