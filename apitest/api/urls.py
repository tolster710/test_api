from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
	url(r'^test', views.test),
	url(r'^create',views.create),
	url(r'^view', views.entry_view),

)
