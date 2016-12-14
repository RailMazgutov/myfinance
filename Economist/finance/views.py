from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from datetime import date

from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from requests import Response

from rest_framework import viewsets
from rest_framework import serializers, views

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.

from .serializers import AccountSerializer, ChargeSerializer, StatsByMonthSerializer
from .models import Account, Charge, User
from .forms import ChargeForm, AccountForm, ProfileForm, PasswordForm
from .decorators import security


#api
class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer

    def get_queryset(self):
        return self.request.user.account.all()


class ChargeViewSet(viewsets.ModelViewSet):
    serializer_class = ChargeSerializer

    def get_queryset(self):
        return Charge.objects.filter(account__user=self.request.user).order_by('_date')


class MonthStatCollection(views.APIView):

    def get(self, request, pk=None):
        charges = Account.objects.get(pk=pk).charges
        months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                  'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        curr_year = date.today().year
        statistics = []
        for month in range(1, 13):
            month_charges = charges.filter(_date__month=month, _date__year=curr_year).all()
            total=0
            for charge in month_charges:
                total += charge.value

            statistic = {'month': months[month - 1], 'amount': total}
            statistics.append(statistic)

        serializer = StatsByMonthSerializer(statistics, many=True)
        return Response(serializer.data)


def accounts(request):
    user = request.user
    if (not user.is_authenticated()):
        context = RequestContext(request,
                             {'request': request,
                              'user': request.user})
        return render_to_response('finance/views/index.html', context_instance=context)
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = user
            account.save()
    else:
        form = AccountForm()

    return render(request,
                  'finance/views/accounts_view.html',
                  {"accounts": user.account.all(), 'form': form, 'user':user})


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
                  'finance/views/account_details_view.html',
                  {'form': form, 'account': account, 'statistics': statistics})

@login_required
def profile(request):
    context = {'name': request.user.username,
               'password': request.user.password,
               'address': request.user.address,
               'email': request.user.email,
               'accounts': request.user.account.all()
               }
    return render(request, 'finance/views/profile.html', context)


@login_required
def profile(request):
    context = {'name': request.user.username,
               'password': request.user.password,
               'address': request.user.address,
               'email': request.user.email,
               'phone_number': request.user.phone_number,
               'id': request.user.id,
               'accounts': request.user.account.all()
               }
    return render(request, 'finance/views/profile.html', context)

@login_required
def profile_form(request, id):
    user = request.user
    info = ''
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            #user.set_password(form.cleaned_data['password'])
            user.save()
            info = 'Изменения сохранены!'
        else:
            info = 'Что-то пошло не так...'
    else:
        form = ProfileForm(instance=user)
    return render(
        request, 'finance/views/profile_form.html',
        {'form': form, 'info': info, 'id': id}
    )

@login_required
def change_login_password(request):
    user = request.user
    info = ''
    if request.method == "POST":
        form = PasswordForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            login(request, user)
            info = 'Логин и пароль были успешно изменены!'
        else:
            info = 'Что-то пошло не так...'
    else:
        form = PasswordForm()
    return render(
        request, 'finance/views/change_login_password.html',
        {'form': form, 'info': info}
    )

@csrf_exempt
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


@csrf_exempt
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

