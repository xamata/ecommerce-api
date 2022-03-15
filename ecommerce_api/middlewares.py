"""Middleware is a framework of hooks into Django's request/response processing.

Middleware is a callable that takes a request and returns a response, like a view"""
from .authentication import Authentication


class CustomAuthMiddleware(object):
    """Custom Authentication Middleware written as a class whose instances are callable"""

    def resolve(self, next, root, info, **kwargs):
        """User check, if user then authenticated"""
        info.context.user = self.authorize_user(info)
        return next(root, info, **kwargs)

    # doesn't receive any reference arg
    @staticmethod
    def authorize_user(info):
        """Begins the authentication process"""
        auth = Authentication(info.context)
        return auth.authenticate()
