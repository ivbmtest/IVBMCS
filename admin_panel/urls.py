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
    path('add_user/',views.crncform,name='add_user'),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)