from django.shortcuts import render
import json
# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from urllib.parse import urlencode
from jose import jwt
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
     token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"

     token_data = {
         'grant_type': 'authorization_code',
         'client_id': settings.AUTH0_CLIENT_ID,
         'client_secret': settings.AUTH0_CLIENT_SECRET,
         'code': code,
         'redirect_uri': settings.AUTH0_CALLBACK_URL,
     }

     token_response = requests.post(token_url, json=token_data).json()
     id_token = token_response.get('id_token')
     user_info = jwt.decode(
        id_token,
        key='',  
        options={"verify_signature": False},
        audience=settings.AUTH0_CLIENT_ID,
        algorithms=["RS256"]
    )
     

     
     role = user_info.get("https://example.com/role") or request.session.pop("preferred_role", "customer")

     
     request.session['user'] = user_info
     request.session['user_role'] = role
    
     return redirect('/')
    

def register_view(request):
      if request.method == "POST":
         email = request.POST.get("email")
         password = request.POST.get("password")
         role = request.POST.get("role", "customer")

         # Store data in session
         request.session["email"] = email
         request.session["password"] = password
         request.session["preferred_role"] = role

         
         return redirect(f"https://{settings.AUTH0_DOMAIN}/authorize?" + urlencode({
             'response_type': 'code',
             'client_id': settings.AUTH0_CLIENT_ID,
             'redirect_uri': settings.AUTH0_CALLBACK_URL,
             'scope': 'openid profile email',
             'screen_hint': 'signup'  
         }))
    
      return render(request, "register.html")
    
     
        

# Login view
def login_view(request):
    
     return redirect(f"https://{settings.AUTH0_DOMAIN}/authorize?" + urlencode({
         'response_type': 'code',
         'client_id': settings.AUTH0_CLIENT_ID,
         'redirect_uri': settings.AUTH0_CALLBACK_URL,
         'scope': 'openid profile email',
     }))
    
    
# Logout view
def logout_view(request):
     request.session.flush()
     return redirect(f"https://{settings.AUTH0_DOMAIN}/v2/logout?" + urlencode({
        'client_id': settings.AUTH0_CLIENT_ID,
        'returnTo': settings.AUTH0_REDIRECT_URI,
    }))
    
