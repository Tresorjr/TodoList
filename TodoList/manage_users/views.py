from django.shortcuts import render


def index(request):
    return render(request, 'manage_users/index.html')
def main(request):
    return render(request, 'manage_users/main.html')
def temp(request):
    return render(request, 'manage_users/temp.html')
def text(request):
    return render(request, 'manage_users/text.html')
  
