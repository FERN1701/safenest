# decorators.py
from functools import wraps
from django.shortcuts import redirect

def role_required(allowed_roles, redirect_url):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.roles not in allowed_roles:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
