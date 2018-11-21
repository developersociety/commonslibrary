from rest_framework.authentication import SessionAuthentication, BaseSessionAuthentication
from rest_framework.authtoken.models import Token


class SessionAuthentication(BaseSessionAuthentication):
    """Session auth with enforced valid auth token."""

    def authenticate(self, request):
        session_auth = super().authenticate(request)

        if session_auth is not None:
            user, auth = session_auth
            is_valid_api_user = Token.objects.filter(user=user).exists()
            if not is_valid_api_user:
                session_auth = None
        
        return session_auth
