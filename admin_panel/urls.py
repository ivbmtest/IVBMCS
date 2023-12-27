from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.Login,name='Login'),
    path('currency/',views.currency,name='currency'),
    path('category/',views.category,name='category'),
    path('country/',views.country,name='country'),
    path('document/',views.document,name='document'),
    path('services/',views.services,name='services'),
    path('dashboard/',views.dashboard,name='dashboard'),
    # path('add_user/',views.crncform,name='add_user'),
    path('logout/',views.logout,name='logout'),
    path('currency/del_currency/<int:id>/',views.del_currency,name='del_currency'),
    path('currency/update_currency/<int:id>/',views.update_currency,name='update_currency'),
    path('category/update_category/<int:id>/',views.update_category,name="update_category"),
    path('category/del_category/<int:id>/',views.del_category,name='del_category'),
    path('category/update_country/<int:id>/',views.update_country,name="update_country"),
    path('category/del_country/<int:id>/',views.delete_country,name='del_country'),
    path('services/update_service/<int:id>/',views.Update_service,name="update_service"),
    path('services/del_service/<int:id>/',views.delete_service,name='del_service'),
    
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)