from django.shortcuts import render, redirect,get_object_or_404
from .models import StudentUser , Recruiter , Job
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from datetime import date
from django.core.exceptions import ObjectDoesNotExist


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



def change_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    # Cleaner way to get object or show 404 error
    recruiter = get_object_or_404(Recruiter, id=pid)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status:
            recruiter.status = status
            recruiter.save()
            messages.success(request, "Recruiter status updated successfully!")
            return redirect('recruiter_pending')

    return render(request, 'change_status.html', {'recruiter': recruiter})


def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  

    error = ""
    success_message = ""
    
    if request.method == 'POST':
        old_password = request.POST['oldpassword']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirmpassword']

        # Ensure that the new password and confirm password match
        if new_password != confirm_password:
            error = "New Password and Confirm Password should match!"
        else:
            try:
                # Check the current password and update if correct
                user = User.objects.get(id=request.user.id)
                
                # Verify if the old password is correct
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    success_message = "Password changed successfully!"
                    return redirect('admin_login')
                    # Update the session to reflect the new password
                    update_session_auth_hash(request, user)

                else:
                    error = "Incorrect current password"

            except User.DoesNotExist:
                error = "User does not exist"

    return render(request, 'change_passwordadmin.html', {'error': error, 'success_message': success_message})


def change_passwordrecruiter(request):  

    error = ""
    success_message = ""
    
    if request.method == 'POST':
        old_password = request.POST['oldpassword']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirmpassword']

        # Ensure that the new password and confirm password match
        if new_password != confirm_password:
            error = "New Password and Confirm Password should match!"
        else:
            try:
                # Check the current password and update if correct
                user = User.objects.get(id=request.user.id)
                
                # Verify if the old password is correct
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    success_message = "Password changed successfully!"
                    return redirect('recruiter_login')
                    # Update the session to reflect the new password
                    update_session_auth_hash(request, user)

                else:
                    error = "Incorrect current password"

            except User.DoesNotExist:
                error = "User does not exist"

    return render(request, 'change_passwordrecruiter.html', {'error': error, 'success_message': success_message})


def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')  

    error = ""
    success_message = ""
    
    if request.method == 'POST':
        old_password = request.POST['oldpassword']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirmpassword']

        # Ensure that the new password and confirm password match
        if new_password != confirm_password:
            error = "New Password and Confirm Password should match!"
        else:
            try:
                # Check the current password and update if correct
                user = User.objects.get(id=request.user.id)
                
                # Verify if the old password is correct
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    success_message = "Password changed successfully!"
                    return redirect('user_login')
                    
                    # Update the session to reflect the new password
                    update_session_auth_hash(request, user)

                else:
                    error = "Incorrect current password"

            except User.DoesNotExist:
                error = "User does not exist"

    return render(request, 'change_passworduser.html', {'error': error, 'success_message': success_message})

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method == "POST":
        jt = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST['enddate']
        sy = request.POST['Salary']
        lgo = request.FILES.get('image')  # Use .get() to avoid KeyError
        ex = request.POST['Expriance']  # Fix spelling in HTML form too
        loc = request.POST['location']
        sk = request.POST['Skills']
        des = request.POST['Description']

        print("Form Data:", jt, sd, ed, sy, lgo, ex, loc, sk, des)
        user = request.user
        recruiter = Recruiter.objects.get(user=user)

        try:
            Job.objects.create(
                recruiter=recruiter,
                start_date=sd,  # Fixed field name
                End_data=ed,  # Fixed field name
                job_title=jt,
                job_salary=sy,
                Image=lgo,  # Assuming 'image' is the field name in the model
                job_description=des,
                job_location=loc,
                job_experience=ex,  # Check if field matches your model
                Skills=sk,  # Assuming lowercase 'skills' is in the model
                Creationdata=date.today()  # Fixed field name
            )
            error = "No"
        except Exception as e:
            print(e)
            error = "Yes"
    return render(request, 'add_job.html', {'error': error})



def edit_jobdetails(request, pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Job.objects.get(id=pid)
    
    if request.method == "POST":
        try:
            jt = request.POST['jobtitle']
            sd = request.POST['startdate']
            ed = request.POST['enddate']
            sy = request.POST['Salary']
            ex = request.POST['Experience']
            loc = request.POST['location']
            sk = request.POST['Skills']
            des = request.POST['Description']

            # Update job fields
            job.job_title = jt
            job.job_salary = sy
            job.job_description = des
            job.job_location = loc
            job.job_experience = ex
            job.Skills = sk

            # Only update image if a new one was uploaded
            if 'image' in request.FILES:
                job.Image = request.FILES['image']

            # Update start date if provided
            if sd:
                job.start_data = sd

            # Update end date if provided
            if ed:
                job.End_data = ed

            job.save()
            error = "No"
        except Exception as e:
            print(e)  # Useful for debugging
            error = "Yes"

    d = {'error': error, 'job': job}
    return render(request, 'edit_jobdetails.html', d)


def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    try:
        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        
        # Fetch jobs related to the recruiter with optimized query
        job = Job.objects.filter(recruiter=recruiter).select_related('recruiter')
        
        context = {'job': job}
        return render(request, 'job_list.html', context)

    except ObjectDoesNotExist:
        # Handle the case when a recruiter is not found for the user
        return redirect('recruiter_login')  # or a custom error page
    
    except Exception as e:
        # Log the error and show a generic error message
        print(f"Error: {e}")
        return render(request, 'job_list.html', {'error': 'An unexpected error occurred.'})



def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    
    data = Recruiter.objects.filter(status = "pending")
    d = {'data': data}
    print(d)
    return render(request, 'recruiter_pending.html',d)


def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    
    data = Recruiter.objects.filter(status = "Active")
    d = {'data': data}
    print(d)
    return render(request, 'recruiter_accepted.html',d)


def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    
    data = Recruiter.objects.filter(status = "Reject")
    d = {'data': data}
    print(d)
    return render(request, 'recruiter_rejected.html',d)

def all_recruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    
    data = Recruiter.objects.all()
    d = {'data': data}
    print(d)
    return render(request, 'all_recruiter.html',d)

def delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    student = User.objects.get(id = pid )
    student.delete()
    return redirect('views_user')


def delete_recruiter(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    recruiter = User.objects.get(id = pid)
    recruiter.delete()
    return redirect('all_recruiter')

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
            
            StudentUser.objects.create(user=user, mobile=C, image=img, gender=G, Type= "student", name = f , email = E)

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
            Recruiter.objects.create(user=user, mobile=C, image=f'{filename}.jpg', gender=G, Type= "Recruiter", company= company , name = f , status = "pending" , email = E)

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


