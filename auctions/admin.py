from django.contrib import admin
from django.contrib.auth import authenticate, login, logout

from .models import Sales,Items,Bid

admin.site.register(Sales)
admin.site.register(Items)
admin.site.register(Bid)
