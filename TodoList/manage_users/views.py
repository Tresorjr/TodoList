from django.shortcuts import render,redirect
from django.core.validators import validate_email
from .models import utilisateur

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
    return render(request, 'manage_users/temp.html')
def text(request):
    return render(request, 'manage_users/text.html')
  
