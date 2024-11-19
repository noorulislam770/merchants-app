from django.contrib.auth.models import User


def salespersons(request):
    """
    Add all salespersons (users) to the template context.
    """
    if request.user.is_authenticated:  # Only add this context for logged-in users
        return {
            'salespersons': User.objects.all()
        }
    return {}
