from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^pricing$', views.pricing, name='pricing'),
    url(r'^pricingfinal$', views.pricingwcheckout, name='pricingwcheckout'),
    url(r'^howitworks$', views.howitworks, name='howitworks'),
#    url(r'^upload/$', views.upload, name='upload'),
    url(r'^import_sheet/', views.import_sheet, name="import_sheet"),
    url(r'^categorize/', views.categorize, name="categorize"),
    url(r'^checkout/', views.checkout, name="checkout"),
    url(r'^getstarted/', views.getstarted, name="getstarted"),
    url(r'^signup/', views.signup, name="signup"),
    url(r'^dashboard/', views.nextsteps, name="nextsteps"),
    url(r'^signup/stepone', views.stepone, name="stepone"),
    url(r'^user-info', views.newuserprocess, name="newuserprocess"),
    url(r'^login', views.loginpage, name="loginpage"),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^newdash', views.newdash, name="newdash"),
    url(r'^connections', views.updateconnection, name="updateconnection"),
    url(r'^workflowstep1', views.workflow, name="workflow"),
    url(r'^workflowstep2', views.workflow2, name="workflow2"),
    url(r'^workflowstep3', views.workflow3, name="workflow3"),
]