from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from datetime import date

from django.template import RequestContext

from .models import Account, Charge, User
from .forms import ChargeForm, AccountForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def security(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        request = args[0]
        pk = kwargs['pk']
        user = request.user
        account = Account.objects.get(pk=pk)
        if account.user == user:
            return func(*args, **kwargs)

        else:
            return HttpResponse('Not yours')

    return wrapper


def accounts(request):
    user = request.user
    if (not user.is_authenticated()):
        context = RequestContext(request,
                             {'request': request,
                              'user': request.user})
        return render_to_response('finance/index.html', context_instance=context)
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = user
            account.save()
    else:
        form = AccountForm()

    return render(request,
                  'finance/accounts_view.html',
                  {"accounts": user.account.all(), 'form': form})


@login_required
@security
def account_details(request, pk):
    account = Account.objects.get(pk=pk)
    if request.method == "POST":
        form = ChargeForm(request.POST)
        if form.is_valid():
            charge = form.save(commit=False)
            account.add_charge(charge)
    else:
        form = ChargeForm()

    charges = account.charges
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
              'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    curr_year = date.today().year
    statistics = []
    for month in range(1, 13):
        month_charges = charges.filter(_date__month=month, _date__year=curr_year).all()
        income = 0
        outcome = 0
        for charge in month_charges:
            if charge.value > 0:
                income += charge.value
            else:
                outcome += charge.value

        statistic = {'month': months[month - 1], 'income': income, 'outcome': outcome}
        statistics.append(statistic)
    return render(request,
                  'finance/account_details_view.html',
                  {'form': form, 'account': account, 'statistics': statistics})


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not (username and password):
        return render(request, 'finance/login.html')
    user = authenticate(username=username, password=password)
    if not user:
        return render(request, 'finance/login.html')
    login(request, user)
    return redirect('/finance/profile')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/')


@login_required
def profile_view(request):
    context = {'name': request.user.username,
               'password': request.user.password,
               'address': request.user.address,
               'email': request.user.email
               }
    return render(request, 'finance/profile.html', context)


def auth(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['login']
            if 'password' in request.POST:
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=401)  # Unauthorized

            else:
                return HttpResponse(status=400)  # BadRequest
        else:
            return HttpResponse(status=400)  # BadRequest


def register(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['login']
            if 'password' in request.POST:
                password = request.POST['password']
                user = User.objects.create_user(username=username, password=password, email='')
                user.phone_number = ''
                user.address = ''
                user.save()
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=401)  #Unauthorized

            else:
                return HttpResponse(status=400)  # BadRequest
        else:
            return HttpResponse(status=400)  # BadRequest
