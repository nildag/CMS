from django.shortcuts import render

# vista home
def home(request):
    return render(request, 'home/home.html')

def profile(request):
    return render(request, 'account/profile.html')
