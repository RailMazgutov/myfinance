from datetime import date

from django.contrib.auth import authenticate, login
from django.shortcuts import render
from requests import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import serializers, views
from rest_framework.decorators import api_view

from RestApi.models import Token
from .serializers import AccountSerializer, ChargeSerializer, StatsByMonthSerializer, TokenSerializer
from finance.models import Account, Charge, User


#api
class MonthStatCollection(views.APIView):

    def get(self, request, token, pk=None):
        user = Token.getUser(int(token))
        if not user:
            return Response(status=status.HTTP_403_FORBIDDEN)


        charges = Account.objects.get(pk=pk).charges
        months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                  'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        curr_year = date.today().year
        statistics = []
        for month in range(1, 13):
            month_charges = charges.filter(transacted_at__month=month, transacted_at__year=curr_year).all()
            total=0
            for charge in month_charges:
                total += charge.value

            statistic = {'month': months[month - 1], 'amount': total}
            statistics.append(statistic)

        serializer = StatsByMonthSerializer(statistics, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def register(request):
    if 'username' in request.POST:
        if 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            email = ""
            if 'email' in request.POST:
                email = request.POST['email']

            phone_number = ''
            if 'phone_number' in request.POST:
                phone_number = request.POST['phone_number']

            address = ''
            if 'address' in request.POST:
                address = request.POST['address']

            user = User.objects.create_user(username=username, password=password, email=email)
            user.phone_number = phone_number
            user.address = address
            user.save()
            if user:
                return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def auth(request):
    if 'username' in request.POST:
        if 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                token = Token.generate_token(user)
                serializer = TokenSerializer(token)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def addAccount(request, token):
    user = Token.getUser(int(token))
    if not user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        total = int(request.POST['total'])
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        number = int(request.POST['number'])
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        name = int(request.POST['name'])
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    account = Account.create(total, name, user, number)
    serializer = AccountSerializer(account)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getAccounts(request, token):
    user = Token.getUser(int(token))
    if not user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    accounts = user.account.all()
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getAccountCharges(request, token, id):
    user = Token.getUser(int(token))
    if not user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        account = user.account.get(pk=id)
        serializer = ChargeSerializer(account.charges.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def addAccountToCharge(request, token, pk):
    user = Token.getUser(int(token))
    if not user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        account = user.account.get(pk=id)
        try:
            amount = int(request.POST['amount'])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            transacted_at = int(request.POST['transacted_at'])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        charge = Charge.create(amount, date(transacted_at))
        account.add_charge(charge)
        return Response(status=status.HTTP_200_OK)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_403_FORBIDDEN)


