from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$',views.index),
	url(r'^register$',views.register),
	url(r'^login$',views.login),
	url(r'^success$',views.success),
	url(r'^add_quote/(?P<id>\d+)$',views.add_quote),
	url(r'^user_info/(?P<id>\d+)$',views.user_info),
	url(r'^delete/(?P<id>\d+)$',views.delete),
	url(r'^add_to_list/(?P<id>\d+)$',views.add_to_list),
	url(r'^remove/(?P<id>\d+)$',views.remove),
	url(r'^logout$',views.logout),

	]