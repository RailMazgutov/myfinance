from django.db import models
from django.conf import settings

import random
# Create your models here.

class Token(models.Model):
    token = models.BigIntegerField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    @staticmethod
    def generate_token(user):
        if Token.objects.filter(user=user).exists():
            return Token.objects.get(user=user)

        token = random.getrandbits(63)
        while not Token.objects.filter(token=token):
            token = random.getrandbits(63)

        token = Token()
        token.token = token
        token.user = user
        return token

    @staticmethod
    def getUser(token):
        try:
            user = Token.objects.get(token=token)
        except Token.DoesNotExist:
            user = None

        return user