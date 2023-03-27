from django.contrib.auth.backends import ModelBackend

from .models import MyUser



class PasswordlessBackend(ModelBackend):

    def authenticate(self, request, phone=None, **kwargs):
        
        user = None         
        try: 
            user = MyUser.objects.get(phone=phone)
            return user
        except MyUser.DoesNotExist:
            return None
       
        

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id = user_id)
        except MyUser.DoesNotExist:
            return None