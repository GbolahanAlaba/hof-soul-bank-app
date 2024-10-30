from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import re
from . models import *
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            return Response({"status": "failed", "message": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper
