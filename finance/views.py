from django.shortcuts import render

from .models import Account
# Create your views here.


def main(request):
    return render(request, 'finance/main.html', {})


def charges(request):
    account = Account.objects.last()
    return render(request, 'finance/charges_view.html', {"account":account})
