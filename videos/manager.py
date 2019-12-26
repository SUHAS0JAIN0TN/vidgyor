from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
        def create_user(self,email,password,name):
                
                if not email:
                        raise ValueError('Email can not be empty')

                user=self.model(
                        email=self.normalize_email(email),
                        name=name
                )
                user.set_password(password)
                user.save()
                return user

        def create_superuser(self,email,password,name):

                user=self.create_user(self,email=email,password=password,name=name)

                user.is_admin=True
                user.save()
                return user