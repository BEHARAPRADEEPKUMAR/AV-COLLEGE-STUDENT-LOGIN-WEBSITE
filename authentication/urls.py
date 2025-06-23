from django.contrib import admin
from django.urls import path, include
from . import views
from .views import profile,notes,about
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path("profile/<str:rollno>/", profile, name="profile"),
    path("index/", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("notes/", views.notes, name="notes"),
    path("exam/", views.exam, name="exam"),
    path('feedback/', views.feedback, name='feedback')
    
]
