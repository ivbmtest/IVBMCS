from django.urls import path
from . import views,dashboard_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('service/',views.service,name='service'),
    path('contact/',views.contact,name='contact'),
    path('service_details/',views.service_details,name='service_details'),
    path('consulting/',views.consulting,name='consulting'),
    
    # Dashboard
    path('user_home/',dashboard_views.user_dash_home,name='user_home'),
    path('allservice/',dashboard_views.all_service,name='allservice'),
    path('myservice/',dashboard_views.my_service,name='myservice'),
    path('notifications/',dashboard_views.notification,name='notifications'),
    path('payments/',dashboard_views.payments,name='payments'),
    
    # Consultation urls
    path('free_consult/',views.initial_consult,name='free_consult'),
    path('free_consult/<str:value>',views.initial_consult,name='free_consult'),
    
    path('consult/<str:value>/',dashboard_views.select_service,name='consult'),
    path('consult/',dashboard_views.select_service,name='consult'),
    path('appointment/',dashboard_views.appointment,name='appointment'),
    path('booking/',dashboard_views.booking,name='booking'), 
    path('payment/',dashboard_views.payment,name='payment'),
    path('upload_doc/',dashboard_views.upload_doc,name='upload_doc'),

    path('login_otp/',views.login_otp, name = "login_otp"),
    path('otp_ver/',views.otp_ver, name = "otp_ver"),
    path('user_dashboard/',dashboard_views.user_login, name = "user_dashboard"),
]