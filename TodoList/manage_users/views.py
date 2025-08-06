from django.shortcuts import render


def index(request):
    return render(request, 'manage_users/index.html')

def main(request):
    return render(request, 'manage_users/mainhtml.html')
