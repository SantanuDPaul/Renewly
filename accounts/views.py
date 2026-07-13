from django.contrib import messages

from django.shortcuts import redirect, render
from django.views import View

from accounts.forms import RegistrationForm

# Create your views here.
class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('register')  # Redirect to login page after successful registration
        return render(request, 'accounts/register.html', {'form': form})