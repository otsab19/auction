from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.http import HttpResponseRedirect
from .models import Items,Sales,Bid
from .forms import Auctionform
# Create your views here.
from django.http import HttpResponse

def add_item(request):
	if request.method == 'POST':
		aform=Auctionform(request.POST,request.FILES)
		if aform.is_valid():
			item_obj=Items()
			item_obj.item_name=aform.cleaned_data["item_name"]
			item_obj.item_title=aform.cleaned_data["item_title"]
			item_obj.item_price=aform.cleaned_data["item_price"]
			item_obj.item_desc=aform.cleaned_data["item_desc"]
			item_obj.item_image=aform.cleaned_data["item_image"]
			item_obj.sales=aform.cleaned_data["sales"]
			item_obj.item_time_add=aform.cleaned_data["item_time_add"]
			item_obj.item_time_end=aform.cleaned_data["item_time_end"]
			item_obj.save()
			#handle_uploaded_file(request.FILES['file'])
			#instance = form.save(commit=False)
			#intance=Items(file_field=request.FILES['file'])
			#instance.save()
			#form.save()
			
	else:
	    aform = Auctionform()
	context={
	"form":aform
	}
	return render(request,"auction_form.html",context)
def index(request):
	products=get_list_or_404(Items)
	context={"pro":products,"title":"AUCTION"}
	return render(request,"index.html",context)