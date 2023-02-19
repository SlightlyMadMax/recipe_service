from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User


def get_authenticated_client():
    user = User.objects.create_user(
        username='foo@foo.foo',
        email='foo@foo.foo',
        password='top_secret'
    )
    token = Token.objects.create(user=user)
    token.save()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    return client
