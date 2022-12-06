from django.conf import settings
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class TrustMeBroAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # print(request.headers)
        username = request.headers.get('Trust-Me')
        # print("username: ", username)
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user with '{username}'")


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request, ):
        token = request.headers.get('Jwt')
        if not token:
            return None
        decode = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256", )
        pk = decode.get('pk')
        if not pk:
            raise AuthenticationFailed("Invalid Tokken")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("Not Found User")
