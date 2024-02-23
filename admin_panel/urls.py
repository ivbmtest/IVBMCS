from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .agent_views import *
from .staff_views import *
from . import admin_views,agent_views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    # path('login/', LoginView.as_view(), name='Login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('login/',views.Login,name='Login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.Logout,name='logout'),
    
    #user management
    # staff
    path('staff/',staff,name='staff'),
    path('staff/del_staff/<int:id>/',del_staff,name='del_staff'),
    path('staff/update_staff/<int:id>/',update_staff,name='update_staff'),
    # agent
    path('agent/',agent_views.agent,name='agent'),
    path('agent/del_agent/<int:id>/',del_agent,name='del_agent'),
    path('agent/update_agent/<int:id>/',update_agent,name='update_agent'),

    path('age_home/',agent_views.age_home,name="age_home"),
    path('age_service/',agent_views.age_service,name="age_service"),
    path('age_notify/',agent_views.age_notify,name="age_notify"),
    path('age_all_services/',agent_views.age_all_service,name="age_all_services"),
    path('age_payments/',agent_views.age_payments,name="age_payments"),
    

    # user
    # path('user/',views.user,name='user'),
    # path('user/del_user/<int:id>/',views.del_user,name='del_user'),
    # path('user/update_user/<int:id>/',views.update_user,name='update_user'),
    # # admin
    path('admin_dashboard/',admin_views.admin,name='admin_dashboard'),
    path('admin_dashboard/del_admin/<int:id>/',admin_views.del_admin,name='del_admin'),
    path('admin_dashboard/update_admin/<int:id>/',admin_views.update_admin,name='update_admin'),
    
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

    #State
    path('state/',views.state,name='state'),
    path('state/update_state/<int:id>/',views.update_state,name="update_state"),
    path('state/del_state/<int:id>/',views.del_state,name='del_state'),
    
    #services
    path('services/',views.services,name='services'),
    path('services/update_service/<int:id>/',views.Update_service,name="update_service"),
    path('services/del_service/<int:id>/',views.delete_service,name='del_service'),

    #document
    path('document/',views.document,name='document'),
    path('document/del_document/<int:id>/',views.del_document,name='del_document'),
    path('document/update_document/<int:id>/',views.update_document,name="update_document"),
    
    #Format
    path('format/',views.format,name='format'),
    path('format/update_format/<int:id>/',views.update_format,name="update_format"),
    path('format/del_format/<int:id>/',views.del_format,name='del_format'),

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