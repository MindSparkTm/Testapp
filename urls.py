from django.conf.urls import url, include
from . import views
from rest_framework import routers
from . import views
from . import api

router = routers.DefaultRouter()



urlpatterns = (
    # urls for Django Rest Framework API
    url(r'^api/v1/', include(router.urls)),

)

urlpatterns += (
    # urls for patientVisit
     url(r'^register/$', views.usersignup.as_view(), name='usersignup'),
     url(r'^emailverify/$', views.emailverification.as_view(), name='emailverify'),
     url(r'^smsverify/$', views.smsverification.as_view(), name='smsverify'),
     url(r'^loginsmsverify/$', views.loginsmsverification.as_view(), name='loginsmsverify'),
     url(r'^loginemailverify/$', views.loginemailverification.as_view(), name='loginemailverify'),

     url(r'^success/$', views.successpage.as_view(), name='success'),
     url(r'^login/$', views.login.as_view(), name='login'),
     url(r'^error/$',views.error.as_view(),name='error')

)