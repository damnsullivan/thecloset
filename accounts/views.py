from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Seu registro foi bem-sucedido! Bem-vindo ao The Closet.')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def custom_password_reset(request):
    template_name = 'accounts/password_reset_form.html'  # Ajuste este caminho conforme necessário
    
    try:
        get_template(template_name)
    except TemplateDoesNotExist:
        messages.error(request, f"Template '{template_name}' não encontrado. Por favor, verifique se o arquivo existe.")
        return redirect('home')  # Redireciona para a página inicial ou outra página apropriada

    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                if 'new_password1' in request.POST:
                    form = SetPasswordForm(user, request.POST)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Sua senha foi redefinida com sucesso.')
                        return redirect('login')
                    else:
                        for field, errors in form.errors.items():
                            for error in errors:
                                messages.error(request, f"{field.capitalize()}: {error}")
                else:
                    form = SetPasswordForm(user)
                    return render(request, template_name, {'form': form, 'username': username})
            except User.DoesNotExist:
                messages.error(request, 'Nome de usuário não encontrado.')
        else:
            messages.error(request, 'Por favor, forneça um nome de usuário.')
    
    return render(request, template_name)