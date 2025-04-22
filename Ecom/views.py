from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
import requests
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
User = get_user_model()


def dashboard(request):
    return render(request, 'dashboard.html')

def add_product(request):
    return render(request,'add_product.html')

def product(request):
    response = requests.get('https://fakestoreapi.com/products')
    products = response.json() if response.status_code == 200 else []
    return render(request, 'products.html', {'products': products})


def callback_view(request):
    code = request.GET.get('code')
    auth0_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
    headers = {'Content-Type': 'application/json'}
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.AUTH0_CLIENT_ID,
        'client_secret': settings.AUTH0_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.AUTH0_CALLBACK_URL,
    }

    response = requests.post(auth0_url, json=data, headers=headers)
    response_data = response.json()

    # Get user info
    userinfo_url = f"https://{settings.AUTH0_DOMAIN}/userinfo"
    userinfo_response = requests.get(userinfo_url, headers={
        'Authorization': f"Bearer {response_data['access_token']}"
    })
    userinfo = userinfo_response.json()

    
    user, created = User.objects.get_or_create(username=userinfo['email'])
    if created:
       
        user.role = 'customer'
        user.save()

    
    request.session['role'] = user.role
    request.session['user'] = userinfo

    return redirect('/')


def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        
        user = User.objects.create_user(username=email, password=password)
        user.role = role
        user.save()

        return redirect('/login')
    
    return render(request, 'register.html')

# Login view
def login_view(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request,username=email, password=password)
        if user is not None:
            login(request, user)
            
            if user.role == 'seller':
                return redirect('add_product')
            else:
                return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')
# Logout view
def logout_view(request):
    request.session.flush()  
    return redirect('/')
