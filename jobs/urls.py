from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('jobs', GetJobs.as_view()),
    path('job/<id>', GetJob.as_view()),
    path('checkUser', CheckUserView.as_view()),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('enroll/<userPK>/<jobPK>', EnrollView.as_view()),
    path('user_courses/<userPK>', GetCoursesByUserView.as_view())
]

