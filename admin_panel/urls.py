from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.Login,name='Login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.Logout,name='logout'),

    #currency
    path('currency/',views.currency,name='currency'),
    path('currency/del_currency/<int:id>/',views.del_currency,name='del_currency'),
    path('currency/update_currency/<int:id>/',views.update_currency,name='update_currency'),
    path('index/', views.index),
    
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
  
    
    
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)