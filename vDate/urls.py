from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^boys/$', views.boys, name='boys'),
	url(r'^girls/$', views.girls, name='girls'),
	url(r'^gifts/$', views.gifts, name='gifts'),
	url(r'^gifts-new/$', views.newGift, name='gifts-new'),
]