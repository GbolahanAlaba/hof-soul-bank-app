from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import re
from . models import *
from rest_framework.exceptions import ValidationError



def handle_exeptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            return Response({"status": "failed", "message": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper


@handle_exeptions
def validate_email(email):
      # Define the regex pattern for email validation
      try:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)
      except:
        return Response({"status": "failed", "message": "Invalid email"})
          

@handle_exeptions
def is_phone_exist(phone):
    try:
        phone = User.objects.filter(phone=phone).exists()
        return Response({"status": "failed", "message": "Phone exists"})
    except User.DoesNotExist:
        pass


def is_valid_phone(phone):
    # NIGERIAN_PHONE_REGEX = re.compile(r'^(?:\+234|0)?(?:70|80|81|90|91|70|71)\d{8}$')
    WORLDWIDE_PHONE_REGEX = re.compile(r'^\+(?:[0-9] ?){6,14}[0-9]$')
    if not WORLDWIDE_PHONE_REGEX.match(phone):
        raise ValidationError({"status": "failed", "message": "Invalid phone number"})

    # If valid, simply pass
    return True
