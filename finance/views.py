from django.shortcuts import render
from datetime import date
from decimal import Decimal
from .models import Account, Charge
from random import randint
from .forms import ChargeForm, AccountForm
# Create your views here.


def random_transactions( ):
    today = date.today( )
    start_date = today.replace(month=1, day=1).toordinal()
    end_date = today.toordinal()
    while True:
        start_date = randint(start_date, end_date)
        random_date = date.fromordinal(start_date)
        if random_date >= today:
            break
        random_value = randint(-10000, 10000), randint(0, 99)
        random_value = Decimal('%d.%d' % random_value)
        yield random_date, random_value




def accounts(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.save()
    else:
        form = AccountForm()

    return render(request,
                  'finance/accounts_view.html',
                  {"accounts": Account.objects.all(), 'form': form})


def account_details(request, pk):
    account = Account.objects.get(pk=pk)
    if request.method == "POST":
        form = ChargeForm(request.POST)
        if form.is_valid():
            charge = form.save(commit=False)
            account.add_charge(charge)
    else:
        form = ChargeForm()

    return render(request,
                  'finance/account_details_view.html',
                  {'form': form, 'account': account})