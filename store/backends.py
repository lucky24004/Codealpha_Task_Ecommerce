from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None  # nothing to check

        try:
            # Match email instead of username
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # If duplicate emails exist, take the first
            user = User.objects.filter(email=username).first()

        # Ensure user is not None before checking password
        if user and user.check_password(password):
            return user
        return None
