from django.contrib.auth.models import User
from account.models import Profile

# Building a custom authentication backend 221 => 194 تسجيل الدخول بواسطة الاميل و اليوزرنيم
class EmailAuthBackend:
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# social Django
# في وظيفة create_profile ، نتحقق من وجود كائن مستخدم ونستخدم
def create_profile(backend, user, *args, **kwargs):
    """
    Create user profile for social authentication
    """
    Profile.objects.get_or_create(user=user)