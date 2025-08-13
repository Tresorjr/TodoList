from django.shortcuts import render,redirect
from django.core.validators import validate_email
from .models import utilisateur,projet,membre,Todo
from django.contrib import messages

def main(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        poste = request.POST.get('poste')
        role = request.POST.get('role')

        # Vérification mot de passe
        if password != password2:
            return render(request, "manage_users/main.html", {"error": "Les mots de passe ne correspondent pas"})

        # Vérification email existant
        if utilisateur.objects.filter(email=email).exists():
            return render(request, "manage_users/main.html", {"error": "Cet email est déjà utilisé"})

        # Création utilisateur
        user = utilisateur(
            first_name=first_name,
            email=email,
            poste=poste,
            role=role
        )
        user.set_password(password)
        user.save()

        print ("success")

        messages.success(request, "Compte créé avec succès. Veuillez vous connecter.")
        return redirect("index")

    return render(request, "manage_users/main.html")




def index(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = utilisateur.objects.get(email=email)
        except utilisateur.DoesNotExist:
            return render(request, "index.html", {"error": "Utilisateur introuvable"})

        if user.check_password(password):
            request.session['user_id'] = user.id
            request.session['role'] = user.role

            if user.role == 'admin':
                return redirect('temp')  # Rediriger vers la page admin
            else:
                return redirect('text')  # Rediriger vers la page membre simple
        else:
            return render(request, "manage_users/index.html", {"error": "Mot de passe incorrect"})

    return render(request, "manage_users/index.html")



def temp(request):
    projects = projet.objects.all()
    members = utilisateur.objects.all()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == "ajout_utilisateur":
            first_name = request.POST.get("first_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            poste = request.POST.get("poste")
            role = request.POST.get("role")  # chef_projet ou membre

            utilisateur.objects.create(
                first_name=first_name,
                email=email,
                password=password,  #  penser à hasher le mot de passe plus tard
                poste=poste,
                role=role
            )
            messages.success(request, "Utilisateur ajouté avec succès !")
            return redirect("temp")

        if form_type == "task":
            title = request.POST.get('title')
            description = request.POST.get('description')
            project_as_id = request.POST.get('project_as')
            assigned_to_id = request.POST.get('assigned_to')
            date = request.POST.get('date')
            priority = request.POST.get('priority')

            print("NEW TASK:", title, description, project_as_id, assigned_to_id, date, priority)

            if not title:
                print("Erreur : titre vide")
                return redirect('temp')

            project = projet.objects.filter(id=project_as_id).first() if project_as_id else None
            member = utilisateur.objects.filter(id=assigned_to_id).first() if assigned_to_id else None

            Todo.objects.create(
                title=title,
                description=description,
                project_as=project,
                assigned_to=member,
                date=date,
                priority=priority
            )

            print("Tâche enregistrée avec succès")
            return redirect('temp')

        elif form_type == "project":
            name_project = request.POST.get('name_project')
            description_project = request.POST.get('description_project')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            member_ids = request.POST.getlist('member_project')

            print("NEW PROJECT:", name_project, description_project, start_date, end_date, member_ids)

            project = projet.objects.create(
                name_project=name_project,
                description_project=description_project,
                start_date=start_date,
                end_date=end_date
            )

            if member_ids:
                project.member_project.set(member_ids)

            print("Projet enregistré avec succès")
            return redirect('temp')

    return render(request, 'manage_users/temp.html', {
        'projects': projects,
        'members': members
    })



       



def text(request):
    return render(request, 'manage_users/text.html')
  
