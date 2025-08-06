# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

User = get_user_model()

@login_required
def register_user_view(request):
    # Seuls les chefs de projet peuvent créer un utilisateur
    if request.user.role != 'chef':
        return HttpResponseForbidden("Accès refusé. Seul le chef de projet peut créer un utilisateur.")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur créé avec succès.")
            return redirect('liste_utilisateurs')  # Redirige vers une page de ton choix
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})
