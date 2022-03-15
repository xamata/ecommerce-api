"""Authenticates the User's token"""
from datetime import datetime
from django.conf import settings
import jwt
from user_controller.models import User


# from django.contrib.auth.models import User


class TokenManager:
    """Managing our token activities"""

    @staticmethod
    # define the get token with expiration, payload, token type
    def get_token(exp, payload, token_type="access"):
        """multiplied by 60 to make seconds to minutes"""
        exp = datetime.now().timestamp() + (exp * 60)

        return jwt.encode(
            {"exp": exp, "type": token_type, **payload},
            settings.SECRET_KEY,  # uses secret key within .env
            algorithm="HS256",
        )

    @staticmethod
    def decode_token(token):
        """Splitting the token apart to be ready for validation"""
        try:
            decoded = jwt.decode(token, key=settings.SECRET_KEY, algorithms="HS256")
        except jwt.DecodeError:
            return None

        if datetime.now().timestamp() > decoded["exp"]:
            return None

        return decoded

    @classmethod
    def get_access(cls, payload):
        """Access token will expire every 1 day and then send in the payload"""
        return cls.get_token(24 * 60, payload)

    @classmethod
    def get_refresh(cls, payload):
        """Refreshes the token after 7 days"""
        return cls.get_token(7 * 24 * 60, payload, "refresh")


class Authentication:
    """Authenticator class"""

    def __init__(self, request):
        """Using request to relate to django's authenticator"""
        self.request = request

    def authenticate(self):
        """Veryifying user's authentication"""
        data = self.validate_request()
        # no data at all returns None
        if not data:
            return None
        # we will be saving the user_id like this in payload
        return self.get_user(data["user_id"])

    def validate_request(self):
        """Passes the authorization through token manager"""
        authorization = self.request.headers.get("AUTHORIZATION", None)

        if not authorization:
            return None
        # usually token is JWT
        token = authorization[4:]
        # decoded_data will be None if token is invalid
        decoded_data = TokenManager.decode_token(token)

        if not decoded_data:
            return None

        return decoded_data

    @staticmethod
    def get_user(user_id):
        """Imports User from User class in models.py"""

        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist():
            return None
