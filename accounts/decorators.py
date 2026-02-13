from django.http import HttpResponseForbidden

def mechanic_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.userprofile.role != 'MECHANIC':
            return HttpResponseForbidden("Mechanic access only")
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.userprofile.role not in ['ADMIN', 'SUPER_ADMIN']:
            return HttpResponseForbidden("Admin access only")
        return view_func(request, *args, **kwargs)
    return wrapper
