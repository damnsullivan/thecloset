from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.core.exceptions import ValidationError

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        try:
            if form.is_valid():
                user = form.save(commit=False)  
                user.save()
                login(request, user)
                messages.success(request, 'Seu registro foi bem-sucedido! Bem-vindo ao The Closet.')
                return redirect('home')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Erro no campo {field}: {error}")
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Ocorreu um erro durante o registro: {str(e)}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def custom_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            verification_code = get_random_string(length=6, allowed_chars='0123456789')
            request.session['reset_code'] = verification_code
            request.session['reset_user_id'] = user.id
            subject = "Código de Verificação para Redefinição de Senha - The Closet"
            message = f"Seu código de verificação é: {verification_code}"
            send_mail(subject, message, 'noreply@thecloset.com', [email])
            print(f"Código de verificação para {email}: {verification_code}")
            messages.success(request, 'Um código de verificação foi enviado para o seu e-mail.')
            return redirect('verify_reset_code')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Não foi encontrado um usuário com este e-mail.')
        except Exception as e:
            messages.error(request, f"Erro ao enviar e-mail: {e}")
            print(f"Erro ao enviar e-mail: {e}")
    
    return render(request, 'accounts/password_reset_form.html')

def verify_reset_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('verification_code')
        stored_code = request.session.get('reset_code')
        user_id = request.session.get('reset_user_id')
        
        if entered_code == stored_code:
            user = CustomUser.objects.get(id=user_id)
            form = SetPasswordForm(user)
            return render(request, 'accounts/password_reset_confirm.html', {'form': form})
        else:
            messages.error(request, 'Código de verificação inválido.')
    
    return render(request, 'accounts/verify_reset_code.html')

def password_reset_confirm(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, 'Sessão inválida. Por favor, reinicie o processo de redefinição de senha.')
        return redirect('custom_password_reset')
    
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            del request.session['reset_code']
            del request.session['reset_user_id']
            messages.success(request, 'Sua senha foi redefinida com sucesso.')
            return redirect('login')
    else:
        form = SetPasswordForm(user)
    
    return render(request, 'accounts/password_reset_confirm.html', {'form': form})

@login_required
def user_profile(request):
    user = request.user
    
    context = {
        'user': user,
    }
    
    return render(request, 'accounts/user_profile.html', context)
