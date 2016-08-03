from django import forms
from .models import Items,Sales,Bid


class Auctionform(forms.ModelForm):
	class Meta:
		model = Items
		fields=["item_name","item_title","item_price","item_desc","item_image","sales","item_time_add","item_time_end"]