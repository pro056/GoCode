from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from models import *
import simplejson
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import requests
from django.http import HttpResponse


class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def createUser (request):
	json_data = JSONParser().parse(request)
	serializer = userSerializer(data=json_data)
	if serializer.is_valid():
		serializer.save()
		return JSONResponse(serializer.data, status=201)
	return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def setHandle (request):
	json_data = json.loads(request.body)
	user = User.objects.get (user_id=json_data["userid"])
	handlesite = json_data["site"]
	handle = json_data["handle"]
	if (handlesite == "codechef"):
		user.chef_handle = handle
	elif (handlesite == "codeforces"):
		user.forces_handle = handle
	elif (handlesite == "topcoder"):
		user.tc_handle = handle
	elif (handlesite == "spoj"):
		user.spoj_handle = handle
	elif (handlesite == "hackerearth"):
		user.hackere_handle = handle
	elif (handlesite == "hackerrank") :
		user.hackerr_handle = handle
	elif (handlesite == "kaggle"):
		user.kaggle_handle = handle

	return JSONResponse(status=201)
	

	