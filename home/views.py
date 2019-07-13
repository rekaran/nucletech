from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm

# Create your views here.
def index(request):
    return render(request, 'home/index.html')


def contact(request):
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


def commingsoon(request):
    return render(request, 'home/comming.html')


def register(request):
    if request.method=="GET":
        form = SignUpForm()
        args = {"form": form}
        return render(request, 'home/register.html', args)
    elif request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Form Saved")
        return HttpResponse("POST")