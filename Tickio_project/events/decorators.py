from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.core.exceptions import PermissionDenied

def organizador_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo == 'organizador':
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap