from django.shortcuts import render,redirect
from django.core.validators import validate_email
from .models import utilisateur,projet,membre,Todo

def index(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        try:
            Utilisateur = utilisateur.objects.get(email=email)
            if utilisateur.password==password:
                request.session['Utilisateur_id'] = Utilisateur.id
                print("reussie 1111")
                return redirect('index')
                
            else:
                return render(request,'manage_users/index.html',{"error":"mot de passe incorrect"})
        except utilisateur.DoesNotExist :
            return render  (request,'manage_users/index.html',{"error":"Email non trouver !"})  

    return render(request, 'manage_users/index.html')


def main(request):
    error = False
    message = ""
    if request.method == "POST":
        print("HEY HOW")
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        role = request.POST.get('role', None)

        try:   #POUR VERIFIER SI LE MAIL EST VALIDE#
            validate_email(email)
        except:
            error= True
    

        print( "NEW POST:", first_name,last_name,email,role,password, ) #POUR TESTER SI LA REQUETE POST MARCHE#

        context = {
            'error' : error,
            'message': message
        }
        if utilisateur.objects.filter(email=email).exists():
            return render(request,'manage_users/main.html',{"error": "cet email est deja utilise !"})
        
        try:
          contact = utilisateur(first_name=first_name, last_name=last_name, email=email, password=password, role=role)
          contact.save()
          contact= utilisateur()
          print("enregistrement reussie") #VERIFIER SI LES UTILISATEUR SON BIEN ENREGISTRER#
        except  Exception as e :
            print("echec") #RENVOI UN MESSAGE D'ECHEC  DANS LA CONSOLE SI NON#

    return render(request, 'manage_users/main.html')



def temp(request):
    projects = projet.objects.all()
    members = membre.objects.all()

    if request.method == 'POST' :
        print("HEY HOW")
        title = request.POST.get('title', None)
        description = request.POST.get('description', None)
        project_id = request.POST.get('project_as', None)
        assigned_to_id = request.POST.get('assigned_to', None)
        date = request.POST.get('date', None)

        print( "NEW POST:", title,description,project_id,assigned_to_id,date, ) #POUR TESTER SI LA REQUETE POST MARCHE#
        project = projet.objects.filter(id=project_id).first() if project_id else None
        member =membre.objects.filter(id=assigned_to_id).first() if assigned_to_id else None
        
        tache = Todo(title=title, description=description, project_as=project,assigned_to=member, date=date)
        tache.save()
        tache= Todo()

        print("enregistrement reussie") #VERIFIER SI LES UTILISATEUR SON BIEN ENREGISTRER#

        return redirect('temp')
        
    return render(request, 'manage_users/temp.html')

def projet_create(request):
    projects = projet.objects.all()
    members = membre.objects.all()

    if request.method == 'POST' :
        print("HEY HOW wow")
        name_project = request.POST.get('name_project')
        description_project = request.POST.get('description_project')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        member_ids = request.POST.get('member_project')

        print( "NEW POST:",name_project,description_project,start_date,end_date,member_ids, ) #POUR TESTER SI LA REQUETE POST MARCHE#

        project = projects.objects.create(name_project=name_project, description_project=description_project, start_date=start_date,end_date=end_date)

        if member_ids :
            project.member_project.set(member_ids)

            project.save()
            print("enregistrement reussie") #VERIFIER SI LES UTILISATEUR SON BIEN ENREGISTRER#
            return redirect('temp')

        
    return render(request, 'manage_users/temp.html')



def text(request):
    return render(request, 'manage_users/text.html')
  
