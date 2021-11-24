from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project
import uuid
import boto3

# Create your views here.

from django.http import HttpResponse

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

def projects_index(request):
  projects = Project.objects.filter(user=request.user)
  return render(request, 'projects/index.html', {'projects': projects})

def projects_detail(request, project_id):
  project = Project.objects.get(id=project_id)
  