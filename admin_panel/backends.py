from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        print('=======UserModel:::::::',UserModel)
        try:
            print(email,'======================>>>>>>>>>>>>>')
            
            user = UserModel.objects.get(email=email)
            if not user.first_name and not user.last_name:
                    user.display_name=email
            else:
                user.display_name=user
            print('--------usertry=>>>>>>',user)
            print('=========passwordtry::::',password)
            
        except UserModel.DoesNotExist:
            return None
        else:
            print('=========passwordelse:::',password)
            try:
                if user.check_password(password):
                    # if not user.first_name and not user.last_name:
                    #     user.display_name=email
                    # else:
                    #     user.display_name=user
                    print('=========passwordelseif:::',password)
                    print('--------user=>>>>>>',user)
                    return user.display_name
            except Exception as e:
                print('-exception::::')
        return None