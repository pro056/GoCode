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
from bs4 import BeautifulSoup
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
	user = User.objects.get(email_id=json_data["email"])
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
	user.save()
	return JSONResponse(json_data, status=400)

def getUsers (request):
	serializer = userSerializerSecure(User.objects.all(), many=True)
	return JSONResponse(serializer.data)


def update(request):
    r = requests.get ("http://www.clist.by")
    data = r.text
    soup = BeautifulSoup(data)
    Past_Contests.objects.all().delete()
    Running_Contests.objects.all().delete()
    Future_Contests.objects.all().delete()
    for link in soup.find_all ('tr'):
        info = []
        contest_status = 0
        for link1 in link.find_all ('td'):
            info.append(link1.text)
        
        
        if (len(info) == 4):
            time = info[0].encode ('ascii', 'ignore')
            start=""
            end=""
            if (len(time) == 41):
                start = time[1:19]
                end = time[20:38]
            elif (len(time) == 39):
                strt = time[1:15]
                stime = time[17:22]
                etime = time[30:35]
                start = strt + " " + stime
                end = strt + " " + etime
            current_time = datetime.now().strftime('%Y.%m.%d %a %H:%M')
            current_time = str(current_time)
            
            if (len(start) > 7):
                if (start[8] < '0' or start[8] > '9'):
                    styear = "20" + start[6:8]
                    enyear = "20" + end[6:8]
                    sthour = start[13:15]
                    stmin = start[16:18]
                    enhour = end[13:15]
                    enmin = end[16:18]
                else :
                    styear = start[6:10]
                    enyear = end[6:10]
                    sthour = start[15:17]
                    enhour = end[15:17]
                    stmin = start[18:20]
                    enmin = end[18:20]
                
                stdate = start[0:2]
                endate = end[0:2]
                stmonth = start[3:5]
                enmonth = end[3:5]
                
                
                
                curr_date = current_time[0:10] + " " + current_time[15:21]
            
                start_time = sthour + ":" + stmin
                end_time = enhour + ":" + enmin
                
                start_date = styear + "." + stmonth + "." + stdate + " " + start_time
                end_date = enyear + "." + enmonth + "." + endate + " " +  end_time
                
                if (start_date > curr_date) : 
                    contest_status = 3
                elif (start_date <= curr_date <= end_date):
                    contest_status = 2
                else :
                    contest_status = 1
                contest_duration = info[1].encode('ascii', 'ignore')
                contest_name = ""
                contest_site = ""
                info1 = []
                
                for link2 in link1.find_all('a'):
                    info1.append(link2.text)
                
                if (len(info1) == 3):
                    contest_name = info1[0].encode('ascii', 'ignore')
                    contest_site = info1[2].encode('ascii', 'ignore')
                if (contest_status == 1):
                    contest = Past_Contests(contest_name = contest_name, contest_duration=contest_duration, contest_start_time=start, contest_end_time=end, contest_site=contest_site)
                    contest.save()
                elif (contest_status == 2):
                    contest = Running_Contests(contest_name = contest_name, contest_duration=contest_duration, contest_start_time=start, contest_end_time=end, contest_site=contest_site)
                    contest.save()
                else :
                    contest = Future_Contests(contest_name = contest_name, contest_duration=contest_duration, contest_start_time=start, contest_end_time=end, contest_site=contest_site)
                    contest.save()
    return HttpResponse(status=201)

def getAllContests(request):
    p_contest = Past_Contests.objects.all()
    r_contest = Running_Contests.objects.all()
    f_contest = Future_Contests.objects.all()
    to_json = []
    for con in p_contest:
        con_dict={}
        con_dict['name'] = con.contest_name
        con_dict['site'] = con.contest_site
        con_dict['duration'] = con.contest_duration
        con_dict['start'] = con.contest_start_time
        con_dict['end'] = con.contest_end_time
        con_dict['status'] = con.contest_status
        to_json.append(con_dict)
    for con in r_contest:
        con_dict={}
        con_dict['name'] = con.contest_name
        con_dict['site'] = con.contest_site
        con_dict['duration'] = con.contest_duration
        con_dict['start'] = con.contest_start_time
        con_dict['end'] = con.contest_end_time
        con_dict['status'] = con.contest_status
        to_json.append(con_dict)
    for con in f_contest:
        con_dict={}
        con_dict['name'] = con.contest_name
        con_dict['site'] = con.contest_site
        con_dict['duration'] = con.contest_duration
        con_dict['start'] = con.contest_start_time
        con_dict['end'] = con.contest_end_time
        con_dict['status'] = con.contest_status
        to_json.append(con_dict)
    response_data = simplejson.dumps(to_json)

    return HttpResponse(response_data,content_type='application/json')


def getPastContests(request):
    p_contest = Past_Contests.objects.all()
    
    to_json = []
    for con in p_contest:
        con_dict={}
        con_dict['name'] = con.contest_name
        con_dict['site'] = con.contest_site
        con_dict['duration'] = con.contest_duration
        con_dict['start'] = con.contest_start_time
        con_dict['end'] = con.contest_end_time
        con_dict['status'] = con.contest_status
        to_json.append(con_dict)

    response_data = simplejson.dumps(to_json)

    return HttpResponse(response_data,content_type='application/json')

def getCurrContests(request):
    p_contest = Running_Contests.objects.all()
    
    to_json = []
    for con in p_contest:
        con_dict={}
        con_dict['name'] = con.contest_name
        con_dict['site'] = con.contest_site
        con_dict['duration'] = con.contest_duration
        con_dict['start'] = con.contest_start_time
        con_dict['end'] = con.contest_end_time
        con_dict['status'] = con.contest_status
        to_json.append(con_dict)

    response_data = simplejson.dumps(to_json)

    return HttpResponse(response_data,content_type='application/json')

def getFutureContests(request):
    p_contest = Future_Contests.objects.all()
    
    to_json = []
    for con in p_contest:
        con_dict={}
        con_dict['name'] = con.contest_name
        con_dict['site'] = con.contest_site
        con_dict['duration'] = con.contest_duration
        con_dict['start'] = con.contest_start_time
        con_dict['end'] = con.contest_end_time
        con_dict['status'] = con.contest_status
        to_json.append(con_dict)

    response_data = simplejson.dumps(to_json)

    return HttpResponse(response_data,content_type='application/json')




	


	

	