from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .agent_views import *

urlpatterns = [
    path('login/',views.Login,name='Login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.Logout,name='logout'),
    
    #user management
    # staff
    # path('staff/',views.staff,name='staff'),
    # path('staff/del_staff/<int:id>/',views.del_staff,name='del_staff'),
    # path('staff/update_staff/<int:id>/',views.update_staff,name='update_staff'),
    # agent
    path('agent/',agent,name='agent'),
    path('agent/del_agent/<int:id>/',del_agent,name='del_agent'),
    path('agent/update_agent/<int:id>/',update_agent,name='update_agent'),
    # user
    # path('user/',views.user,name='user'),
    # path('user/del_user/<int:id>/',views.del_user,name='del_user'),
    # path('user/update_user/<int:id>/',views.update_user,name='update_user'),
    # # admin
    # path('admin/',views.admin,name='admin'),
    # path('admin/del_admin/<int:id>/',views.del_admin,name='del_admin'),
    # path('admin/update_admin/<int:id>/',views.update_admin,name='update_admin'),
    

    #currency
    path('currency/',views.currency,name='currency'),
    path('currency/del_currency/<int:id>/',views.del_currency,name='del_currency'),
    path('currency/update_currency/<int:id>/',views.update_currency,name='update_currency'),
    # path('index/', views.index),
    
    #category
    path('category/',views.category,name='category'),
    path('category/update_category/<int:id>/',views.update_category,name="update_category"),
    path('category/del_category/<int:id>/',views.del_category,name='del_category'),

    #country
    path('country/',views.country,name='country'),
    path('country/update_country/<int:id>/',views.update_country,name="update_country"),
    path('country/del_country/<int:id>/',views.delete_country,name='del_country'),
    # path('add_user/',views.crncform,name='add_user'),
    
    #services
    path('services/',views.services,name='services'),
    path('services/update_service/<int:id>/',views.Update_service,name="update_service"),
    path('services/del_service/<int:id>/',views.delete_service,name='del_service'),

    #document
    path('document/',views.document,name='document'),
    path('document/del_document/<int:id>/',views.del_document,name='del_document'),
    path('document/update_document/<int:id>/',views.update_document,name="update_document"),

    #TaxDetails
    path('taxdetails/',views.taxdetails,name='taxdetails'),
    path('taxdetails/update_taxdetails/<int:id>/',views.update_taxdetails,name="update_taxdetails"),
    path('taxdetails/del_taxdetails/<int:id>/',views.delete_taxdetails,name='del_taxdetails'),

    #Taxmaster
    path('taxmaster/',views.taxmaster,name='taxmaster'),
    path('taxmaster/update_taxmaster/<int:id>/',views.update_taxmaster,name="update_taxmaster"),
    path('taxmaster/del_taxmaster/<int:id>/',views.delete_taxmaster,name='del_taxmaster'),
  
#Order Details
    path('orders',views.orders,name='orders'),
#demo user
    path('user/',views.demo_user,name='demo_user'),

#my task
    path('task/',views.my_task,name='task'),
    path('select_task/<int:id>/',views.select_my_task,name='select_task'),
    path('task_detail/<int:id>/',views.task_details,name='task_detail'),
  
    path('profile/',views.profile,name='profile'),  


    path('total_ord/',views.total_ord,name='total_ord'),    
  
    
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)