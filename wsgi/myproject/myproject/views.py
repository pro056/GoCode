from django.shortcuts import render
import requests
import json
from serializers import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from models import *
import simplejson
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
	serializer = userSerializer (data=json_data)
	if (serializer.is_valid()) :
		serializer.save()
		serializer1 = userSerializerSecure(data=json_data)
		if serializer1.is_valid():
			return JSONResponse(serializer1.data, status=400)
		return JSONResponse(serializer1.errors, status=400)
	return JSONResponse(serializer.errors, status = 400)

@csrf_exempt
def setHandle (request):
	json_data = JSONParser().parse(request)
	user = User.objects.filter(user_id=json_data["user_id"])
	handleSite = json_data["handleSite"]
	handle = json_data["handle"]
	if (handleSite == 'codechef'):
		user.chef_handle = handle
	elif (handleSite == 'codeforces') :
		user.forces_handle = handle
	elif (handleSite == 'topcoder'):
		user.tc_handle = handle
	elif (handleSite == 'spoj') :
		user.spoj_handle = handle
	elif (handleSite == 'hackerearth'):
		user.hackere_handle = handle
	elif (handleSite == 'hackerrank'):
		user.hackerr_handle = handle
	elif (handleSite ==  'kaggle'):
		user.kaggle_handle = handle 
#	user.save()
	return JSONResponse(user, status=400)

def getUsers (request):
	serializer = userSerializerSecure(User.objects.all(), many=True)
	return JSONResponse(serializer.data)
	


	

	