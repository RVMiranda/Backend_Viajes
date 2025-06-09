from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import AuthToken

class TokenAuthentication(BaseAuthentication):
    keyword = "Token"

    def authenticate(self, request):
        auth = request.headers.get("Authorization", "").split()
        if len(auth) != 2 or auth[0] != self.keyword:
            return None
        token = auth[1]
        try:
            tok = AuthToken.objects.get(token=token, expires__gt=timezone.now())
        except AuthToken.DoesNotExist:
            raise exceptions.AuthenticationFailed("Token inválido o expirado")
        return (tok.user, tok)
