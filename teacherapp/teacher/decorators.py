from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test



# def unauthenticated_user(view_func):
#     def wrapper_func(request,*args, **kwargs):
#         if request.user.is_authenticated:
#             if request.user.is_teacher:
#                 return redirect('teacherProfileUpdate')
#             elif request.user.is_student:
#                 return redirect('studentProfileUpdate')
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrapper_func




def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_student,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_teacher,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
