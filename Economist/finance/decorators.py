from django.http import HttpResponse

from .models import Account


def security(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        request = args[0]
        pk = kwargs['pk']
        user = request.user
        account = Account.objects.get(pk=pk)
        if account.user == user or user in account.onwers.all():
            return func(*args, **kwargs)

        else:
            return HttpResponse(status=401)

    return wrapper
