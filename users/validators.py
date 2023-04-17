import datetime

from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import ValidationError


def check_birth_date(birth_date):
    year_dif = relativedelta(datetime.date.today(), birth_date).years
    if year_dif < 9:
        raise ValidationError(f"У пользователя возраст {year_dif} лет! Разрешено только с 9-ти!")


def check_email(email):
    if "rambler.ru" in email.split("@")[-1]:
        raise ValidationError("Регистрация с домена rambler.ru запрещена!")