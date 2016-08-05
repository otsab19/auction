from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import Items,Sales,Bid
from .forms import Auctionform,Userform
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.http import HttpResponse

def add_item(request):			#adding items by user				
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
			return redirect('index')
				
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
				return render(request, 'login.html', {'error_message':'Account Deactivaated'})
		else:
			return render(request, 'login.html', {'error_message':'Invalid Login'})
	return render(request, 'login.html')

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
				login(request,user)
				
				return render(request, 'register.html')
	context = {'form':form}
	return render(request, 'register.html', context)
def my_auctions(request):
	user = request.user
	products=Items.objects.all().filter(user=request.user)
	#products=get_list_or_404(Items).filter(user=request.user)
	context={"pro":products,"user":user}
	return render(request,"my_auctions.html",context)

def home(request):
	user = request.user
	products=get_list_or_404(Items)
	context={"pro":products,"title":"AUCTION"}
	return render(request,"home.html",context)


