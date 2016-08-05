from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add_item, name='add_item'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^my_auctions/$', views.my_auctions, name='my_auctions'),
    url(r'^home/$', views.home, name='home')

]
