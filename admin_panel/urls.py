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
    path('taxmaster/',views.taxmaster,name='taxmaster'),
    path('taxdetails/',views.taxdetails,name='taxdetails'),
    # path('add_user/',views.crncform,name='add_user'),
    path('logout/',views.Logout,name='logout'),
    #add curre
    #path('add_curr/',views.add_currency,name='add_curr'),
    # del_currency
    path('del_currency_js/',views.del_currency_js,name='del_currency'),
    path('currency/del_currency/<int:id>/',views.del_currency,name='del_currency'),
    path('select_del/',views.select_del,name='select_del'),


    path('curr_ser/',views.curr_ser,name='ser'),
    path('curr_ser2/',views.curr_ser2,name='curr_ser'),


    #pagination
    path('paginated_and_filtered_data/', views.paginated_and_filtered_data, name='paginated_and_filtered_data'),
    path('sample/',views.sample,name='sample'),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)