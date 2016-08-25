from django import forms
from .models import Items,Sales,Bid
from django.contrib.auth.models import User


class Userform(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username','email','password']

class Auctionform(forms.ModelForm):
	item_date_end= forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
	item_time_end= forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
	class Meta:
		model = Items
		fields=["item_name","item_title","item_price","item_desc","item_image","sales","item_date_end","item_time_end"]

class Bidform(forms.ModelForm):
	class Meta:
		model=Bid
		fields=["bid_amt"]