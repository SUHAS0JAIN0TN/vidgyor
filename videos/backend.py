from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

User=get_user_model()

class NewBackend:
        
        def authenticate(self,request,email,password):
                try:
                        user=User.objects.get(email=email)

                        if user.check_password(password) and user.is_active:
                                return user
                        else:
                                return None

                except User.DoesNotExist:
                        return None
                        # raise e
                        


                



        def get_user(self,user_id):
                try:
                        user=User.objects.get(id=user_id)
                        if(user.is_active):
                                return user
                        else:
                                return None
                except User.DoesNotExist:
                        return None