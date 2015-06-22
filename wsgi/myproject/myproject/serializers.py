from django.forms import widgets
from rest_framework import serializers

class userSerializer (serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('user_id','password','first_name','last_name','email_id')