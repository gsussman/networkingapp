from django.conf.urls import url
from . import views

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
    url(r'^nextsteps/', views.nextsteps, name="nextsteps")
]