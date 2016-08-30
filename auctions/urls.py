from django.conf.urls import url
from django.contrib.auth.models import Permission, User
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_item/$', views.add_item, name='add_item'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^my_auctions/$', views.my_auctions, name='my_auctions'),
    url(r'^home/$', views.home, name='home'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^(?P<item_id>[0-9]+)/bid/$', views.bid, name='bid'),
    url(r'^(?P<item_id>[0-9]+)/delete_bid/$', views.delete_bid, name='delete_bid')

]
