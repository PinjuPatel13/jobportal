from django.shortcuts import render, redirect
from .models import StudentUser , Recruiter
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def test_session(request):
    return HttpResponse(f"User authenticated: {request.user.is_authenticated}")

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        request.session.flush()
        print("User logged out and session flushed")
    else:
        print("User was already logged out")
    return redirect('user_login')

def views_user(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    data = StudentUser.objects.all()
    d = {'data': data}
    return render(request, 'views_user.html',d)

def admin_login(request):
    error = ""
    
    if request.method == 'POST':
        username = request.POST.get('Uname')
        password = request.POST.get('Pwd')
        
        print(f"Attempting login with username: {username}")  
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_staff:  
                login(request, user)
                print(f"Admin login successful: {user.username}")
                return redirect('admin_home')
            else:
                error = "not_admin"
                print(f"User {user.username} is not an admin.")
        else:
            error = "invalid_credentials"
            print("Invalid username or password.")
    
    return render(request, 'admin_login.html', {'error': error})

def admin_home(request):
   return render(request, 'admin_home.html')

def User_signup(request):
    error = ""
    success_message = ""  
    if request.method == "POST":
        f = request.POST['Uname']
        L = request.POST['LastName']
        E = request.POST['Email']
        C = request.POST['ContactNumber']
        P = request.POST['Pwd']
        G = request.POST['Gender']
        img = request.FILES['Image']
        print("Form Data:", f, L, E, C, P, G, img)

        try:
            if User.objects.filter(username=E).exists():
                error = "Yes"
                success_message = "This email is already registered. Please use a different email."
                return render(request, 'User_signup.html', {'error': error, 'success_message': success_message})

            user = User.objects.create_user(first_name=f, username=E, password=P, last_name=L)
            
            StudentUser.objects.create(user=user, mobile=C, image=img, gender=G, Type= "student", name = f)

            error = "no"  
            success_message = "Signup successful! You will be redirected to the login page shortly."
            return render(request, 'User_signup.html', {'error': error, 'success_message': success_message})

        except IntegrityError as e:
          
            error = "Yes"
            success_message = f"Error: {str(e)} - This might be due to duplicate email. Please try again."
            print("Integrity Error:", e)
        except Exception as e:
            error = "Yes"
            success_message = f"There was an error during sign up: {str(e)}. Please try again."
            print("General Error:", e)

    return render(request, 'User_signup.html', {'error': error, 'success_message': success_message})


def user_login(request):
    error = ""
    success_message = ""
    if request.method == 'POST': 
        N = request.POST.get('Uname')  
        Ps = request.POST.get('Pwd')
        print(f"Attempting login with Username: {N}, Password: {Ps}")
        
        user = authenticate(username=N, password=Ps)
        
        if user is not None:
            print(f"User authenticated: {user.username}")
            try:
                user1 = StudentUser.objects.get(user=user)
                print(f"User type: {user1.Type}")
                
                if user1.Type == "student":
                    login(request, user) 
                    error = "no"  
                    success_message = "Login successful!"
                    return redirect('user_home')
                else:
                    error = "not_student"  
                    print("User is not a student")
            except StudentUser.DoesNotExist:
                error = "no_student_user"
                print("Student user record not found")
        
        else:
            error = "invalid_credentials"
            print("Invalid username or password")


    return render(request, 'user_login.html', {'error': error, 'success_message': success_message})

@login_required(login_url='user_login')
def user_home(request):
    print(f"User authenticated: {request.user.is_authenticated}")
    return render(request, 'user_home.html')


def recruiter_login(request):
    print("🚀 recruiter_login view called!")
    error = ""
    success_message = ""
    
    if request.method == 'POST': 
        print(request.POST)
        N = request.POST.get('Uname')  
        Ps = request.POST.get('Pwd')

        user = authenticate(username=N, password=Ps)
        print(f"Authenticated user: {user}")  # Check if the user is authenticated

        if user is not None:
            try:
                user1 = Recruiter.objects.get(user=user)
                print(f"Recruiter object: {user1}")  # Debug recruiter object
                print(f"Recruiter Type: {user1.Type}")  # Confirm Type field
                
                if user1.Type == "Recruiter" and  user1.status != "pending":
                    login(request, user)
                    error = "no"
                    success_message = "Login Successfully!"
                    print("Redirecting to recruiter_home")
                    return redirect('recruiter_home')
                else:
                    error = "not_recruiter"  
                    print("User is not a recruiter")
            except Recruiter.DoesNotExist:
                error = "no_recruiter"
                print("No recruiter record found")
        else:
            error = "invalid_credentials"
            print("Invalid username or password")

    return render(request, 'recruiter_login.html', {'error': error, 'success_message': success_message})

def recruiter_signup(request):
    error = ""
    success_message = ""  
    if request.method == "POST":
        f = request.POST['Uname']
        L = request.POST['LastName']
        E = request.POST['Email']
        C = request.POST['ContactNumber']
        P = request.POST['Pwd']
        G = request.POST['Gender']
        img = request.FILES.get('Image')
        company = request.POST['company']

        print("Form Data:", f, L, E, C, P, G, img,company)

        try:
            if User.objects.filter(username=E).exists():
                error = "Yes"
                success_message = "This email is already registered. Please use a different email."
                return render(request, 'recruiter_signup.html', {'error': error, 'success_message': success_message})

            user = User.objects.create_user(first_name=f, username=E, password=P, last_name=L)
            
            filename = get_random_string(length=32)
            default_storage.save(f'{filename}.jpg', ContentFile(img.read()))
            Recruiter.objects.create(user=user, mobile=C, image=f'{filename}.jpg', gender=G, Type= "Recruiter", company= company , name = f , status = "pending")

            error = "no"  
            success_message = "Signup successful! You will be redirected to the login page shortly."
            return render(request, 'recruiter_login.html', {'error': error, 'success_message': success_message})
        except IntegrityError as e:
          
            error = "Yes"
            success_message = f"Error: {str(e)} - This might be due to duplicate email. Please try again."
            print("Integrity Error:", e)
        except Exception as e:
            error = "Yes"
            success_message = f"There was an error during sign up: {str(e)}. Please try again."
            print("General Error:", e)

    return render(request, 'recruiter_signup.html', {'error': error, 'success_message': success_message})
    

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    return render(request, 'recruiter_home.html')


