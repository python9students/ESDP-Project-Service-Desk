from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from source.accounts.forms import MyUserCreationForm

User = get_user_model()


class RegisterView(CreateView):
    model = User
    template_name = "registration.html"
    form_class = MyUserCreationForm

    def register_view(request, *args, **kwargs):
        if request.method == 'POST':
            form = MyUserCreationForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('webapp:index')
        else:
            form = MyUserCreationForm()
        return render(request, 'registration.html', context={'form': form})
