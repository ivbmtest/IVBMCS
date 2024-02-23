
from admin_panel.models import *

def select_service(request):
    # category=ctgry.objects.all()
    category = ctgry.objects.prefetch_related('srvc_set').all()
    print(">>>>>>>>>>>>>>>>",category)
    return {'category':category}

