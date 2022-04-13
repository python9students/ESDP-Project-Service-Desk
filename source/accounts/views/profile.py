from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import redirect, render

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect('ticket:service_object_list')
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ticket:service_object_list')
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('ticket:service_object_list')

