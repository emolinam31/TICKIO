from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Vista simple de login
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

# Vista simple de registro
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # No necesitamos crear explícitamente el perfil porque
            # lo manejamos en el método save() de CustomUser
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Vista simple de perfil
@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado!')
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

# Vista simple de logout
def logout_view(request):
    logout(request)
    messages.info(request, '¡Has cerrado sesión!')
    return redirect('home')