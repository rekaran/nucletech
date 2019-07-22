from django.http import HttpResponse, Http404, JsonResponse
from builder.models import Profile, Project
from builder.views import save_ipref
from django.shortcuts import render
from django.conf import settings
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import numpy as np
import requests
import json
import time
import sys
import re

# Mongo Databse Connection
client = MongoClient(settings.DATABASE_URL)
dbData = client['dataManager']

# Mongo Collections
dbraw = dbData.raw
dbshielded = dbData.shielded
dbmetamorph = dbData.metamorph
dbflowpool = dbData.flowpool
dbfaqpool = dbData.faqpool
dbdatapools = dbData.datapools
dbsmalltalks = dbData.smalltalks
dbkeymapper  = dbData.keymapper

# Create your views here.
def tokenize(data):
    rgx = re.compile(r"[#\w']+")
    word_list = rgx.findall(data)
    word_list = [w.lower() for w in word_list]
    return word_list

def mlVocab(dataset):
    vocab = []
    ner_dicts = {}
    for key, data in dataset.items():
        for d in data:
            token = tokenize(d)
            vocab+=token
            ner_list = [n for n in token if n[0]=="#"]
            if len(ner_list)>0:
                ner_dicts[key] = ner_list
    vocab = list(sorted(set(vocab)))
    return vocab, ner_dicts

def mlTensor(dataset):
    vocab, ner_dicts = mlVocab(dataset) # Required
    len_vocab = len(vocab)
    intent = list(dataset.keys())
    tensor_word = np.zeros([len_vocab, len_vocab], dtype=int)
    tensor_word_intent = np.zeros([len_vocab, len(intent)], dtype=int)
    np.seterr(divide='ignore', invalid='ignore')
    ner_vocab = []
    ner_dict = {}
    variation_mapper = {}
    for key, value in dataset.items():
        for data in value:
            variation_mapper[data] = key
            token = tokenize(data)
            for i, t in enumerate(token):
                first_index = vocab.index(t)
                tensor_word_intent[first_index][intent.index(key)]+=1
                if len(token) > 1:
                    if i+1 < len(token):
                        if token[i+1][0]=="#":
                            ner_vocab.append(token[i+1])
                            if t in (ner_dict.keys()):
                                if token[i+1] in list(ner_dict[t].keys()):
                                    ner_dict[t][token[i+1]]+=1
                                else:
                                    ner_dict[t][token[i+1]]=1
                            else:
                                ner_dict[t]={token[i+1]: 1}
                        second_index = vocab.index(token[i+1])
                        tensor_word[first_index][second_index]+=1
    ner_vocab = list(sorted(set(ner_vocab)))
    ner_keys = list(sorted(ner_dict.keys())) # Required
    tensor_ner = np.zeros([len(ner_keys), len(ner_vocab)], dtype=int)
    for key, value in ner_dict.items():
        key_index = ner_keys.index(key)
        for k, v in value.items():
            k_index = ner_vocab.index(k)
            tensor_ner[key_index][k_index] = v
    tensor_ner_ = (tensor_ner.T/tensor_ner.sum(axis=1)).T
    tensor_ner_ = np.nan_to_num(tensor_ner_) # Required
    tensor_word_ = (tensor_word.T/tensor_word.sum(axis=1)).T
    tensor_word_ = np.nan_to_num(tensor_word_) # Required
    tensor_word_intent_ = (tensor_word_intent.T/tensor_word_intent.sum(axis=1)).T
    tensor_word_intent_ = np.nan_to_num(tensor_word_intent_) # Required
    pheremone = {
        "vocab": vocab,
        "tensor_word": tensor_word_.tolist(),
        "ner_keys": ner_keys,
        "tensor_word_intent": tensor_word_intent_.tolist(),
        "ner_dicts": ner_dicts,
        "tensor_ner": tensor_ner_.tolist()
    }
    p_dump = json.dumps(pheremone)
    p_size = sys.getsizeof(p_dump)
    return pheremone, p_size, intent, variation_mapper
    

def getdata(request, name):
    try:
        api_key = request.META["HTTP_TOKEN"]
        if request.method == "POST":
            data = json.loads(request.body)
            profile = Profile.objects.get(api_key=api_key)
            if profile.user.email == request.user.email:
                project_hash = data["key"]
                project_id = data["hash"]
                try:
                    faq_data = dbfaqpool.find({"projectId": project_id, "projectHash": project_hash}).sort('timestamp', -1)
                    faq_data = faq_data.next()
                except Exception as e:
                    faq_data = {"data": []}
                try:
                    flow_data = dbflowpool.find({"projectId": project_id, "projectHash": project_hash}).sort('timestamp', -1)
                    flow_data = flow_data.next()
                except Exception as e:
                    flow_data = {"data": []}
                try:
                    st_data = dbsmalltalks.find({"projectId": project_id, "projectHash": project_hash}).sort('timestamp', -1)
                    st_data = st_data.next()
                except Exception as e:
                    st_data = dbsmalltalks.find_one({"default": True, "createdBy": "nucletech"})
                try:
                    data_martix = dbdatapools.find({"projectId": project_id, "projectHash": project_hash}).sort('timestamp', -1)
                    data_martix = data_martix.next()
                    del data_martix["_id"]
                except Exception as e:
                    data_martix = {}
                return JsonResponse({"success": 200, "flow": flow_data["data"], "faq": faq_data["data"], "smalltalk": st_data["data"], "datamatrix": dict(data_martix)}, safe=False)
        raise Http404
    except Exception as e:
        print(e)
        raise Http404


def savedata(request, name):
    # try:
    api_key = request.META["HTTP_TOKEN"]
    if request.method == "POST":
        print(type(request.body.decode("utf-8")))
        data = json.loads(request.body.decode("utf-8"))
        profile = Profile.objects.get(api_key=api_key)
        if profile.user.email == request.user.email:
            flow_data = data["flow"]
            faq_data = data["faq"]
            st_data = data["smalltalks"]
            project_hash = data["key"]
            project_id = data["hash"]
            project = Project.objects.get(user=request.user, project_id=project_id, project_hash=project_hash)
            start_time = time.time()
            train_data = {}
            encode_data = {}
            flow_data_ = {}
            for flow in flow_data:
                flow_name = "flow_"+flow["name"].replace(" ", "_").lower()
                train_data[flow_name] = flow["variation"]
                stage_data = {idx: stage for idx, stage in enumerate(flow["stages"])}
                flow_data_[flow_name] = stage_data
            for faq in faq_data:
                if faq["active"]:
                    train_data["faq_"+faq["name"]] = faq["variation"]
                    encode_data["faq_"+faq["name"]] = faq["answer"]
            for st in st_data:
                if st["active"]:
                    train_data["faq_"+st["name"]] = st["variation"]
                    encode_data["faq_"+st["name"]] = st["answer"]
            pheremone, p_size, intent, variation = mlTensor(train_data)
            train_time = time.time()-start_time
            timestamp = int(datetime.timestamp(datetime.today()))
            post = requests.post(url="https://www.nuclechat.com/encode/nucletech.com".format(request.user.domain), data={"data": json.dumps(encode_data), "key": project_hash, "hash": project.project_key, "intent": json.dumps(intent), "variation": json.dumps(variation), "flow": json.dumps(flow_data_)}, headers={"Authorization": project_hash, "origin": "nucletech.com"})
            shielded = json.loads(post.text.decode("utf-8"))
            post = dbflowpool.insert_one({"projectId": project_id, "projectHash": project_hash,"data": flow_data, "timestamp": timestamp, "domain": request.user.domain}).inserted_id
            post = dbfaqpool.insert_one({"projectId": project_id, "projectHash": project_hash, "data": faq_data, "timestamp": timestamp, "domain": request.user.domain}).inserted_id
            post = dbraw.insert_one({"projectId": project_id, "projectHash": project_hash, "data": train_data, "timestamp": timestamp, "domain": request.user.domain}).inserted_id
            post = dbsmalltalks.insert_one({"projectId": project_id, "projectHash": project_hash, "data": st_data, "timestamp": timestamp, "domain": request.user.domain}).inserted_id
            post = dbdatapools.insert_one({"projectId": project_id, "projectHash": project_hash, "trainTime": train_time, "metamorphSize": p_size, "trainTimestamp": timestamp, "timestamp": timestamp, "domain": request.user.domain}).inserted_id
            post = dbmetamorph.insert_one({"projectId": project_id, "projectHash": project_hash, "data": pheremone, "timestamp": timestamp}).inserted_id
            post = dbshielded.insert_one(shielded).inserted_id
            keymap = dbkeymapper.find_one_and_update({"hash": project_hash}, {"$set": {"saveTimestamp": timestamp}})
            # post = dbkeymapper.
            post = save_ipref(request)
            print(train_time, p_size)
            return JsonResponse({"status": 200})
        print("Here")
        raise Http404
    # except Exception as e:
    #     print(e)
    #     raise Http404


def index(request):
    raise Http404