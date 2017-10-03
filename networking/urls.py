from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
#    url(r'^upload/$', views.upload, name='upload'),
    url(r'^import_sheet/', views.import_sheet, name="import_sheet"),
    url(r'^categorize/', views.categorize, name="categorize"),
]