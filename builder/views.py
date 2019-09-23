from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from pymongo import MongoClient
import httpagentparser
from .models import *
import requests
import hashlib
import string
import random
import json

# Mongo Databse Connection
client = MongoClient(settings.DATABASE_URL)
dbResource = client['resourceManager']
dbData = client['dataManager']

randomPool = string.ascii_uppercase + string.ascii_lowercase + string.digits

def extract_request_info(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', "")
    userAgent = request.META.get('HTTP_USER_AGENT')
    user_details = httpagentparser.detect(userAgent)
    return (ip, userAgent, user_details)

def get_geoloc(ipaddress):
    return requests.get("https://api.hostip.info/get_json.php?ip={}&position=true".format(ipaddress)).json()


def save_ipref(request):
    (ipaddress, agent, user_details) = extract_request_info(request)
    geo_loc = get_geoloc(ipaddress)
    ip = Ipaddress()
    ip.user = request.user
    ip.ipaddress = ipaddress
    ip.user_agent = agent
    ip.browser = json.dumps(user_details["browser"])
    ip.os = json.dumps(user_details["os"])
    ip.platform = json.dumps(user_details["platform"])
    ip.is_bot = user_details["bot"]
    ip.geo_location = json.dumps(geo_loc)
    ip.save()
    return True


# Create your views here.
def index(request):
    if request.method == "GET":
        # if request.user.is_verified:
        project_list=[]
        projects = ProjectAuth.objects.filter(user=request.user).order_by("-date_created")
        for project in projects:
            p = Project.objects.get(id=project.project.id)
            tmpProject = {"name": p.project_name, "status": p.is_live, "chats": 123456, "user": 1234, "analyze": project.analytics_view, "human": project.human_view, "retrain": p.retrain_date, "key": p.project_key}
            project_list.append(tmpProject)
        return render(request, 'builder/index.html', {'projects': project_list})
        # return redirect('builder.index')
    elif request.method == "POST":
        if request.user.is_verified:
            projectName = request.POST['project-name']
            projectName = projectName.replace(" ", "").upper()
            suplimentKey = ''.join(random.choice(randomPool) for _ in range(15))
            projectKey = ''.join(random.choice(randomPool) for _ in range(256))
            projectId = "{}_{}$ats7jsdh{}".format(projectName, request.user.id, suplimentKey)
            digest = hashlib.md5(projectId.encode()).digest()
            whirlpool = hashlib.new('whirlpool')
            whirlpool.update(digest)
            hashKey = whirlpool.hexdigest()
            post = requests.post(url="https://www.nuclechat.com/hash_encode/{}".format(request.user.domain), data={"hash": hashKey})
            project = Project()
            project.user = request.user
            project.project_id = projectId
            project.project_name = projectName
            project.project_hash = hashKey
            project.project_hash_enc = post.text
            project.project_key = projectKey
            project.language = json.dumps(["en"])
            project.timezone = "UTC"
            project.voice_out = json.dumps({"gender": "Male", "pitch": "Young"})
            project.billing_amount = "0"
            project.save()
            authorization = ProjectAuth()
            authorization.user = request.user
            authorization.project = project
            authorization.builder_view = True
            authorization.builder_edit = True
            authorization.is_creator = True
            authorization.save()
            post = save_ipref(request)
            return redirect('builder.index')
        return redirect('builder.index')

    
def edit(request, name):
    name = name.upper()
    try:
        project = Project.objects.get(user=request.user, project_name=name)
        profile = Profile.objects.get(user=request.user)
        return render(request, 'builder/edit.html', {'project_name': name, "project_key": project.project_hash, "project_hash": project.project_id, "api_key": profile.api_key})
    except Exception as e:
        print(e)
        return redirect('builder.index')


def profile(request):
    data = {"accesskey": "asd", "coupon": None}
    return render(request, 'builder/profile.html', data)