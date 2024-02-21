from . models import *

"""function to get the current user details in user dashboard"""

def get_user_details(current_user):
    print("current user :: :::",current_user.email)
    if '@' in current_user.email:
        current_user = userdata.objects.get(email = current_user)
    else:
        current_user = userdata.objects.get(phone_number = current_user)
    return current_user