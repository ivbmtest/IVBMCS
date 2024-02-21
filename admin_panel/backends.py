from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        print('=======UserModel:::::::',UserModel)
        try:
            print(email,'======================>>>>>>>>>>>>>')
            
            user = UserModel.objects.get(email=email)
            print('--------usertry=>>>>>>',user)
            print('=========passwordtry::::',password)
            
        except UserModel.DoesNotExist:
            return None
        else:
            print('=========passwordelse:::',password)
            try:
                if user.check_password(password):
                    print('=========passwordelseif:::',password)
                    print('--------user=>>>>>>',user)
                    return user
            except Exception as e:
                print('-exception::::')
        return None