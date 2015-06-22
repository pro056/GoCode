from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from models import *
import simplejson
from rest_framework import *
import requests
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def createUser (request):
	json_data = json.loads (request.body)
	newUser = User(user_id=json_data["userid"], password=json_data["passwd"], first_name=json_data["fname"], last_name=json_data["lname"], email_id=json_data["email"])
	newUser.save()
	return JSONResponse (status=201)

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
	

	
