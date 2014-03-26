from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def has_erp_profile(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    	Decorator for views that checks that the user has erp_profile
    """
    actual_decorator = user_passes_test(
        lambda u: has_attr(u, "erp_profile") and hasattr(u, "profile"),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def has_profile(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    	Decorator for views that checks that the user has a user profile
    """
    actual_decorator = user_passes_test(
        lambda u: u.has_attr("profile"),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
