from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
# from htmlmin.decorators import minified_response
from django.shortcuts import render, redirect
from .forms import SignUpForm

# Create your views here.
# @minified_response
def index(request):
    return render(request, 'home/index.html')


# @minified_response
def contact(request):
    return render(request, 'home/contact.html')


# @minified_response
def about(request):
    return render(request, 'home/about.html')


# @minified_response
def termsofuse(request):
    return render(request, 'home/termsofuse.html')


# @minified_response
def commingsoon(request):
    return render(request, 'home/comming.html')


# @minified_response
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