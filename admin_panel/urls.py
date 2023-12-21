from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index,name='index'),
    path('currency/',views.currency,name='currency'),
    path('category/',views.category,name='category'),
    path('country/',views.country,name='country'),
    path('documemt/',views.document,name='document'),
    path('services/',views.services,name='services'),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)