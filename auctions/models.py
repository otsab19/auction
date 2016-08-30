from django.db import models
from django.contrib.auth.models import Permission, User

# Create your models here.
class Sales(models.Model):
	product_id = models.AutoField(primary_key=True)
	product_cat = models.CharField(max_length=100)
	
	def __str__(self):
		return self.product_cat

class Items(models.Model):
	user = models.ForeignKey(User, default=1)
	item_id = models.AutoField(primary_key=True,max_length=100)
	item_name = models.CharField(max_length=100)
	item_title = models.CharField(max_length=100)
	item_price = models.IntegerField()
	item_desc = models.CharField(max_length=100)
	item_image = models.FileField()
	sales = models.ForeignKey(Sales,on_delete=models.CASCADE)
	item_time_add = models.DateTimeField()
	item_date_end = models.DateField()
	item_time_end = models.TimeField()

	def __str__(self):
		return str(self.item_name)


class Bid(models.Model):
	auction_id= models.AutoField(primary_key=True)
	#auction_product=models.ForeignKey(Items,on_delete=models.CASCADE)
	bid_amt=models.IntegerField()
	bid_time=models.DateTimeField()
	user = models.ForeignKey(User, default=1)
	bid_item = models.ForeignKey(Items,blank=True,null=True,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.bid_item) + " " + str(self.user)


