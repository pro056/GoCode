from django.forms import widgets
from rest_framework import serializers
from models import User

class userSerializer (serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('user_id','password','first_name','last_name','email_id', 'chef_handle','tc_handle','forces_handle','spoj_handle','hackere_handle','hackerr_handle',
	'kaggle_handle')