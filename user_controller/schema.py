import graphene
from .models import User
from graphene_django import DjangoObjectType
from django.contrib.auth import authenticate
from datetime import datetime
from ecommerce_api.authentication import TokenManager


class UserType(DjangoObjectType):
    """Uses Django framework for our custom schema"""

    class Meta:
        """Meta class"""

        model = User


class RegisterUser(graphene.Mutation):
    """Mutation is adding to the GraphQL Query"""

    status = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        """Adding these parameteres to the Query"""

        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    def mutate(self, info, email, password, **kwargs):
        """create the user"""
        User.objects.create_user(email, password, **kwargs)

        return RegisterUser(status=True, message="User created successfully")


class LoginUser(graphene.Mutation):
    """Changing info for an already existing user"""

    access = graphene.String()
    refresh = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        """Adding these parameters to the Query"""

        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        """Mutation of the user info"""
        user = authenticate(username=email, password=password)

        if not user:
            raise Exception("Invalid credentials")

        user.last_login = datetime.now()
        user.save()
        # token variables are created
        access = TokenManager.get_access({"user_id": user.id})
        refresh = TokenManager.get_refresh({"user_id": user.id})

        return LoginUser(access=access, refresh=refresh, user=user)


class GetAccess(graphene.Mutation):
    """Getting Access token put into graphql"""

    access = graphene.String()

    class Arguments:
        """putting the refresh token inside of grphaql format"""

        refresh = graphene.String(required=True)

    def mutate(self, info, refresh):
        """Changing the graphql values"""
        token = TokenManager.decode_token(refresh)

        if not token or token["type"] != "refresh":
            raise Exception("Invalid token or has expired")

        access = TokenManager.get_access({"user_id": token["user_id"]})

        return GetAccess(access=access)


class Query(graphene.ObjectType):
    """Query of our project"""

    users = graphene.List(UserType)

    def resovlve_users(self, info, **kwargs):
        return User.objects.all()


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    get_access = GetAccess.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
