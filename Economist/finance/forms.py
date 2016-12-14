from django import forms
from datetime import date
from .models import Charge, Account, User
from django.core.exceptions import ValidationError
import re


class ChargeForm(forms.ModelForm):
    _value = forms.DecimalField(label = 'Value', required = True)
    _date = forms.DateField(label = 'Date', required = True)

    class Meta:
        model = Charge
        fields = ("_date", "_value")


class AccountForm(forms.ModelForm):
    _total = forms.DecimalField(label='Начальное состояние', required = True)
    name = forms.CharField(label='Имя счета', max_length=20)
    class Meta:
        model = Account
        fields = ("_total", "name")


class ProfileForm(forms.ModelForm):
    #username = forms.CharField(label='Логин', max_length=16, min_length=5)
    first_name = forms.CharField(label='Имя', max_length=16)
    last_name = forms.CharField(label='Фамилия', max_length=16)
    address = forms.CharField(label='Адрес', max_length=50)
    phone_number = forms.CharField(label='Телефонный номер', max_length=16)
    email = forms.CharField(label='Электронная почта', max_length=32)
    #password = forms.CharField(label='Пароль', min_length=8)
    class Meta:
        model = User
        fields = ("address", "phone_number", "email", "first_name", "last_name")
    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        phone_number = cleaned_data.get('phone_number')
        email = cleaned_data.get('email')
        if re.fullmatch(r'\+[1-9][0-9]{10}', phone_number) and len(phone_number) == 12:
            if re.fullmatch(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
                return cleaned_data
            else:
                self.add_error('email', "Неверный формат адреса электронной почты")
                raise ValidationError("Неверный формат адреса электронной почты")
        else:
            self.add_error('phone_number', "Неверный формат телефонного номера")
            raise ValidationError("Неверный формат телефонного номера")


class PasswordForm(forms.ModelForm):
    username = forms.CharField(label='Логин', max_length=16, min_length=5)
    password = forms.CharField(label='Пароль', min_length=8)
    class Meta:
        model = User
        fields = ("username", "password")
    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if re.fullmatch(r'[a-zA-Z0-9]{5,16}', username):
            if re.fullmatch(r'[a-zA-Z0-9]{8,}', password):
                return cleaned_data
            else:
                self.add_error('password', "Пароль должен состоять только из цифр и латинских букв")
                raise ValidationError("Пароль должен состоять только из цифр и латинских букв")
        else:
            self.add_error('username', "Логин должен состоять только из цифр и латинских букв")
            raise ValidationError("Логин должен состоять только из цифр и латинских букв")


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин', max_length=16, min_length=5)
    password = forms.CharField(label='Пароль', min_length=8)
    first_name = forms.CharField(label='Имя', max_length=16)
    last_name = forms.CharField(label='Фамилия', max_length=16)
    address = forms.CharField(label='Адрес', max_length=50)
    phone_number = forms.CharField(label='Телефонный номер', max_length=16)
    email = forms.CharField(label='Электронная почта', max_length=32)
    class Meta:
        model = User
        fields = ("username", "password", "address", "phone_number", "email", "first_name", "last_name")
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        phone_number = cleaned_data.get('phone_number')
        email = cleaned_data.get('email')
        if re.fullmatch(r'[a-zA-Z0-9]{5,16}', username):
            if re.fullmatch(r'[a-zA-Z0-9]{8,}', password):
                if re.fullmatch(r'\+[1-9][0-9]{10}', phone_number) and len(phone_number) == 12:
                    if re.fullmatch(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
                        return cleaned_data
                    else:
                        self.add_error('email', "Неверный формат адреса электронной почты")
                        raise ValidationError("Неверный формат адреса электронной почты")
                else:
                    self.add_error('phone_number', "Неверный формат телефонного номера")
                    raise ValidationError("Неверный формат телефонного номера")
            else:
                self.add_error('password', "Пароль должен состоять только из цифр и латинских букв")
                raise ValidationError("Пароль должен состоять только из цифр и латинских букв")
        else:
            self.add_error('username', "Логин должен состоять только из цифр и латинских букв")
            raise ValidationError("Логин должен состоять только из цифр и латинских букв")