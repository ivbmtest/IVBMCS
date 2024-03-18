
from admin_panel.models import *
import datetime

def select_service(request):
    # category=ctgry.objects.all()
    category = ctgry.objects.prefetch_related('srvc_set').all()
    #print(">>>>>>>>>>>>>>>>",category)
    return {'category':category}

def copyright_year(request):
    current_year = datetime.datetime.now().year
    return {"copyright_year":current_year}