from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

# class RollNoBackend(ModelBackend):
#     def authenticate(self, request, rollno=None, password=None, **kwargs):
#         if rollno is None or password is None:
#             return None

#         try:
#             user = User.objects.get(rollno=rollno)  # Ensure 'rollno' is in your User model
#             if user.check_password(password):
#                 return user
#         except User.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None

# User = get_user_model()
        
from django.contrib.auth.backends import BaseBackend
from django.conf import settings
from django.apps import apps

import django
django.setup()  # Ensure Django apps are loaded before using models

CustomUser = apps.get_model('authentication', 'CustomUser')  # Dynamically get model

class RollnoBackend(BaseBackend):
    def authenticate(self, request, rollno=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(rollno=rollno)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None



from django.conf import settings
print(settings.INSTALLED_APPS)
print("RollnoBackend loaded successfully")
