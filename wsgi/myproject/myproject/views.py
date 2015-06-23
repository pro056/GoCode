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
	serializer = userSerializer(data=json_data)
	if (User.objects.filter(user_id=json_data["user_id"])) :
		user = User.objects.filter (user_id=json_data["user_id"]).delete()
	serializer1 = userSerializerSecure(data=json_data)
	if serializer.is_valid():
		serializer.save()
		if (serializer1.is_valid()):
			serializer1.save()
			return JSONResponse(serializer1.data, status=400)
		return JSONResponse(serializer.errors, status=400)
	return JSONResponse(serializer.errors, status=400)



	

	