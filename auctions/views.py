from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import Items,Sales,Bid
from .forms import Auctionform,Userform,Bidform
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.http import JsonResponse
from django.db.models import Q
import datetime
# Create your views here.
from django.http import HttpResponse
from django.utils import timezone
from django.db import IntegrityError
from django.db.models import Max,Count

def add_item(request):			#adding auction item by user				
	if request.method == 'POST':
		aform=Auctionform(request.POST,request.FILES)
		if aform.is_valid():
			item_obj=Items()
			item_obj.user=request.user
			item_obj.item_name=aform.cleaned_data["item_name"]
			item_obj.item_title=aform.cleaned_data["item_title"]
			item_obj.item_price=aform.cleaned_data["item_price"]
			item_obj.item_desc=aform.cleaned_data["item_desc"]
			item_obj.item_image=aform.cleaned_data["item_image"]
			item_obj.sales=aform.cleaned_data["sales"]
			item_obj.item_time_add=datetime.datetime.now()
			item_obj.item_date_end=aform.cleaned_data["item_date_end"]
			item_obj.item_time_end=aform.cleaned_data["item_time_end"]
			dt=datetime.datetime.combine(item_obj.item_date_end,item_obj.item_time_end)
			if (dt<datetime.datetime.now()):
				context={"form":aform,"error_message":"type proper date"}
				return render(request,"auction_form.html",context)
			else:
				item_obj.save()
			#handle_uploaded_file(request.FILES['file'])
			#instance = form.save(commit=False)
			#intance=Items(file_field=request.FILES['file'])
			#instance.save()
			#form.save()
			return redirect('home')
				
	else:
	    aform = Auctionform()
	    
	context={
	"form":aform
	}
	return render(request,"auction_form.html",context)
def index(request):#main page
	products=Items.objects.all()
	query=request.GET.get("q")
	if query:
		products=products.filter (Q(item_name__icontains=query)).distinct()

		context={"pro":products,"title":"AUCTION"}
		return render(request,"index.html",context)
	
	context={"pro":products,"title":"AUCTION"}
	return render(request,"index.html",context)

def logout_user(request):
	user = request.user
	logout(request)
	form = UserForm(request.POST or None)
	context = {
		'form':form
	}
	#return render(request, 'login.html', context)
	return redirect('index')


def login_user(request):
	if request.method == "POST":
		
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
	 		if user.is_active:
	 			login(request,user)
					
	 			return redirect('home')
	 		else:
	 			return render(request, 'index.html', {'error_message':'Account Deactivaated'})
		else:
	 		return redirect('index')
	return render(request, 'index.html',{'error_message':'Invalid Login'})
	 	#return JsonResponse({'uname':user.username, 'pass':user.password})

def register(request):
	form = Userform(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username = username, password=password)
		if user is not None:
			if user.is_active:
				login_user(request)
				
				#return render(request,"index.html")
				return redirect('home')
	context = {'form':form}
	return render(request, 'register.html', context)
def my_auctions(request):#show action added by a user
	user = request.user
	products=Items.objects.all().filter(user=request.user)
	#products=get_list_or_404(Items).filter(user=request.user)
	context={"pro":products,"user":user}
	return render(request,"my_auctions.html",context)

def home(request):
	query = request.GET.get("q")
	user = request.user
	products=Items.objects.all().exclude(user=user)
	
	if query:
		products=products.filter (Q(item_name__icontains=query)).distinct()
		context={"pro":products,"title":"AUCTION"}
		return render(request,"home.html",context)

	
	context={"pro":products,"title":"AUCTION"}
	return render(request,"home.html",context)


def logout_user(request):
	logout(request)
	
	#return render(request, 'index.html', context)
	return redirect('index')

def bid(request,item_id): #bidding page

	cu_datetime=datetime.datetime.now()
	pr=Items.objects.get(pk=item_id)
	max_bid=Bid.objects.filter(bid_item=pr).aggregate(Max('bid_amt'),Count('bid_amt',))#returns dictionary
	print(max_bid)
	m=max_bid['bid_amt__max']#retreiving maximum bid for the item from the dictionary above
	count=max_bid['bid_amt__count']
	print(count)
	max_user=Bid.objects.filter(bid_item=pr).annotate(Max('bid_amt'))
	
	b=Bid.objects.filter(bid_item=pr)
	for bi in b:
		print(bi.bid_amt)

	try:	
		us=b[0].user	
		te=b[0].bid_amt	
		for i in range(1,count):
			if (b[i].bid_amt > te):
				te=b[i].bid_amt
				us=b[i].user
	except:
		us=request.user	
	print(us)
	
	# temp=max_user[0]
	# print(temp)
	# # for i in range(1,count):
	# #  	if(temp<max_user[i]):
	# #  		temp=max_user[i]
	# print(max_user[0].bid_amt__max)
	# print(max_user)
	# print(temp)
	all_bids=Bid.objects.filter(bid_item=pr) #all bids of the particular item
	dt=datetime.datetime.combine(pr.item_date_end,pr.item_time_end)
	if request.method == 'POST':
		bid_form=Bidform(request.POST or None)
		if bid_form.is_valid():
			bid_obj=Bid()
			if((bid_form.cleaned_data["bid_amt"]<pr.item_price)):#checks if bid is greater than the price allocated
				context={'cu_datetime':cu_datetime,'cu_date':dt,'all_bids':all_bids,"pro":pr,'form':bid_form,"error_message":"Bid more than original price"}
				return render(request,"bid.html",context)

			for bi in all_bids:#checks if the bid is more than the previous bids
				if((bid_form.cleaned_data["bid_amt"]<pr.item_price) or (bid_form.cleaned_data["bid_amt"]<bi.bid_amt)):
					context={'cu_datetime':cu_datetime,'cu_date':dt,'all_bids':all_bids,"pro":pr,'form':bid_form,"error_message":"Bid more than previous bidders"}
					return render(request,"bid.html",context)
				
			bid_obj.bid_amt=bid_form.cleaned_data["bid_amt"]
			bid_obj.bid_item=pr
			bid_obj.bid_time=datetime.datetime.now()
			bid_obj.user=request.user
			bid_obj.save()
			return redirect('bid',item_id)
	else:
	    bid_form = Bidform()		
	
	current_user=request.user
	
	context={'us':us,'max_bid':m,'cu_datetime':cu_datetime,'cu_date':dt,"pro":pr,'form':bid_form,'all_bids':all_bids,'cu':current_user}
	return render(request,"bid.html",context)

def delete_bid(request,item_id):
	cu_user=request.user
	pr=Items.objects.get(pk=item_id)
	bid=Bid.objects.filter(bid_item=pr)
	b=bid.filter(user=cu_user)
	b.delete()
	return redirect('bid',item_id)