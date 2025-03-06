from django.shortcuts import render, redirect,get_object_or_404
from .models import StudentUser , Recruiter , Job,Apply
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

def latest_job(request):
    job = Job.objects.all().order_by('-start_data')
    d = {'job': job}
    return render(request, 'latest_job.html',d)

def user_latest_job(request):
    job = Job.objects.all().order_by('-start_data')
    user = request.user
    student = StudentUser.objects.get(user = user)
    data = Apply.objects.filter(student = student)
    li=[]
    for i in data:
        li.append(i.job.id)
    d = {'job': job,'li':li}
    return render(request, 'user_latest_job.html',d)

def job_details(request,pid):
    job = Job.objects.get(id = pid)
    d = {'job': job}
    return render(request, 'job_details.html',d)


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
        lgo = request.FILES.get('image') 
        ex = request.POST['Expriance']  
        loc = request.POST['location']
        sk = request.POST['Skills']
        des = request.POST['Description']

        print("Form Data:", jt, sd, ed, sy, lgo, ex, loc, sk, des)
        user = request.user
        try:
            recruiter = Recruiter.objects.get(user=user)
        except Recruiter.DoesNotExist:
            print(f"No recruiter found for user: {user}")
            error = "Recruiter profile not found. Please complete your profile."
            return render(request, 'add_job.html', {'error': error})


        try:
            Job.objects.create(
                recruiter=recruiter,
                start_data=sd,  
                End_data=ed,  
                job_title=jt,
                job_salary=sy,
                Image=lgo,
                job_description=des,
                job_location=loc,
                job_experience=ex,  
                Skills=sk,  
                Creationdata=date.today()  
            )
            error = "No"
        except Exception as e:
            print(e)
            error = "Yes"
    return render(request, 'add_job.html', {'error': error})



def change_logo(request, pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')  

    try:
        job = Job.objects.get(id=pid)  
    except ObjectDoesNotExist:
       
        return redirect('recruiter_login') 

    error = ""
    
    if request.method == "POST":
        if 'logo' in request.FILES:
            cl = request.FILES['logo']
            job.Image = cl  
            job.save()  
            error = "No"  
        else:
            error = "Yes"  

    d = {'error': error, 'job': job}
    return render(request, 'change_logo.html', d)



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

            if 'image' in request.FILES:
                job.Image = request.FILES['image']

            if sd:
                job.start_data = sd

            if ed:
                job.End_data = ed

            job.save()
            error = "No"
        except Exception as e:
            print(e)  
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
            
            StudentUser.objects.create(user=user, mobile=C, image=img, gender=G, Type= "student", first_name = f , email = E, last_name = L)

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
    if not request.user.is_authenticated:
        return redirect('user_login')

    try:
        student = StudentUser.objects.get(user=request.user)

        if request.method == "POST":
            fn = request.POST['Uname']
            ln = request.POST['LastName']
            cont = request.POST['ContactNumber']
            email = request.POST['Email_ID']
            g = request.POST['Gender']
            img = request.FILES.get('Image')

            student.first_name = fn
            student.last_name = ln
            student.mobile = cont
            student.email = email
            student.gender = g

            if img:
                student.image = img

            student.save()
            messages.success(request, "Profile updated successfully!")  # Message is here
            return redirect('user_home')

    except Recruiter.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('user_login')

    except Exception as e:
        print(e)
        messages.error(request, "An unexpected error occurred.")

    return render(request, 'user_home.html', {'student': student})


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
            Recruiter.objects.create(user=user, mobile=C, image=f'{filename}.jpg', gender=G, Type= "Recruiter", company= company , first_name = f ,last_name = L, status = "pending" , email = E)

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

    try:
        recruiter = Recruiter.objects.get(user=request.user)

        if request.method == "POST":
            fn = request.POST['Uname']
            ln = request.POST['LastName']
            cont = request.POST['ContactNumber']
            comp = request.POST['Company']
            email = request.POST['Email_ID']
            g = request.POST['Gender']
            img = request.FILES.get('Image')

            recruiter.first_name = fn
            recruiter.last_name = ln
            recruiter.mobile = cont
            recruiter.company = comp
            recruiter.email = email
            recruiter.gender = g

            if img:
                recruiter.image = img

            recruiter.save()
            messages.success(request, "Profile updated successfully!")  # Message is here
            return redirect('recruiter_home')

    except Recruiter.DoesNotExist:
        messages.error(request, "Recruiter not found.")
        return redirect('recruiter_login')

    except Exception as e:
        print(e)
        messages.error(request, "An unexpected error occurred.")

    return render(request, 'recruiter_home.html', {'recruiter': recruiter})
