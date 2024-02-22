from . models import *

"""function to get the current user details in user dashboard"""

def get_user_details(current_user):
    print("current user :: :::",current_user.email)
    if '@' in current_user.email:
        current_user = CustomUser.objects.get(email = current_user.email)
    else:
        current_user = CustomUser.objects.get(phone_number = current_user)
    return current_user