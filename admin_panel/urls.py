from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.Login,name='Login'),
    path('currency/',views.currency,name='currency'),
    path('category/',views.category,name='category'),
    path('country/',views.country,name='country'),
    path('documemt/',views.document,name='document'),
    path('services/',views.services,name='services'),
    path('dashboard/',views.dashboard,name='dashboard'),
    # path('add_user/',views.crncform,name='add_user'),
    path('logout/',views.logout,name='logout'),
    #add curre
    #path('add_curr/',views.add_currency,name='add_curr'),
    # del_currency
    path('del_currency/',views.del_currency,name='del_currency'),
    path('select_del/',views.select_del,name='select_del'),


    path('curr_ser/',views.curr_ser,name='ser'),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)