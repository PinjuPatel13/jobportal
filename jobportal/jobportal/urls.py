"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('admin_login/',admin_login, name="admin_login"),
    path('admin_home/',admin_home, name="admin_home"),
    path('user_login/',user_login, name="user_login"),
    path('views_user/',views_user, name="views_user"),
    path('recruiter_pending/',recruiter_pending, name="recruiter_pending"),
    path('change_status/<int:pid>',change_status, name="change_status"),
    path('change_passwordadmin/',change_passwordadmin, name="change_passwordadmin"),
    path('change_passworduser/',change_passworduser, name="change_passworduser"),
    path('change_passwordrecruiter/',change_passwordrecruiter, name="change_passwordrecruiter"),
    path('delete_user/<int:pid>',delete_user, name="delete_user"),
    path('delete_recruiter/<int:pid>',delete_recruiter, name="delete_recruiter"),
    path('add_job/',add_job, name="add_job"),
    path('job_list/',job_list, name="job_list"),
    path('latest_job/',latest_job, name="latest_job"),
    path('user_latest_job/',user_latest_job, name="user_latest_job"),
    path('job_details/<int:pid>',job_details, name="job_details"),
    path('edit_jobdetails/<int:pid>',edit_jobdetails, name="edit_jobdetails"),
    path('change_logo/<int:pid>',change_logo, name="change_logo"),
    path('applyforjob/<int:pid>',applyforjob, name="applyforjob"),
    path('applied_candidate_list/',applied_candidate_list, name="applied_candidate_list"),
    path('contact/',contact, name="contact"),



    path('recruiter_login/', recruiter_login, name="recruiter_login"),
    path('recruiter_accepted/', recruiter_accepted, name="recruiter_accepted"),
    path('recruiter_rejected/', recruiter_rejected, name="recruiter_rejected"),
    path('all_recruiter/', all_recruiter, name="all_recruiter"),

    
    path('User_signup/', User_signup, name='signup'),
    path('recruiter_signup/', recruiter_signup, name='recruiter_signup'),
    path('user_home/', user_home, name='user_home'),
    path('recruiter_home/', recruiter_home, name='recruiter_home'),
    path('logout/', Logout, name='logout'),
    path('test-session/', test_session,name = "test_session"),


    
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

