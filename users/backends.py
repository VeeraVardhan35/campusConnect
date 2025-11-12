from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to fetch user by email or username
            user = User.objects.get(
                Q(email=username) | Q(username=username)
            )
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # If multiple users found, get the first one
            users = User.objects.filter(
                Q(email=username) | Q(username=username)
            )
            for user in users:
                if user.check_password(password):
                    return user
        return None