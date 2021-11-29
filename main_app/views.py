from django.contrib.auth.models import User
from django.db.models import fields
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project, Resource, Step, Wireframe
from .forms import StepForm
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'coding-cooler-freezer-drawer'

# Create your views here.
class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

@login_required
def projects_index(request):
  projects = Project.objects.filter(user=request.user)
  return render(request, 'projects/index.html', {'projects': projects})

@login_required
def projects_detail(request, project_id):
  project = Project.objects.get(id=project_id)
  resources_not_in_project = Resource.objects.exclude(id__in = project.resources.all().values_list('id'))
  step_form = StepForm()
  return render(request, 'projects/detail.html', {
    'project': project, 
    'step_form': step_form, 
    'resources': resources_not_in_project,
  })

class ProjectCreate(LoginRequiredMixin, CreateView):
  model = Project
  fields = ['name', 'programming_language', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ProjectUpdate(LoginRequiredMixin, UpdateView):
  model = Project
  fields = ['name', 'programming_language', 'description']

class ProjectDelete(LoginRequiredMixin, DeleteView):
  model = Project
  success_url = '/projects/'

@login_required
def add_step(request, project_id):
  form = StepForm(request.POST)
  if form.is_valid():
    new_step = form.save(commit=False)
    new_step.project_id = project_id
    new_step.save()
  return redirect('projects_detail', project_id=project_id)

# @login_required
# def delete_step(request, project_id):
#   form = StepForm(request.POST)



class ResourceCreate(LoginRequiredMixin, CreateView):
  model = Resource
  fields = '__all__'

class ResourceList(LoginRequiredMixin, ListView):
  model = Resource

class ResourceDetail(LoginRequiredMixin, DetailView):
  model = Resource

class ResourceUpdate(LoginRequiredMixin, UpdateView):
  model = Resource
  fields = ['name', 'url']

class ResourceDelete(LoginRequiredMixin, DeleteView):
  model = Resource
  success_url = '/resources/'

@login_required
def assoc_resource(request, project_id, resource_id):
  Project.objects.get(id=project_id).resources.add(resource_id)
  return redirect('projects_detail', project_id=project_id)

@login_required
def add_wireframe(request, project_id):
  wireframe_file = request.FILES.get('wireframe-file', None)
  if wireframe_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + wireframe_file.name[wireframe_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(wireframe_file, BUCKET, key)
      url = f'{S3_BASE_URL}{BUCKET}/{key}'
      wireframe = Wireframe(url=url, project_id=project_id)
      project_wireframe = Wireframe.objects.filter(project_id = project_id)
      if project_wireframe.first():
        project_wireframe.first().delete()
      wireframe.save()
    except Exception as err:
      print('An error occured sending a picture to s3 dipshit: %s' %err)
  print('wireframe', wireframe_file)
  return redirect('projects_detail', project_id=project_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('parts_index')
    else:
      error_message = 'I have no idea how you messed up typing words into a box, but you did. Try again einstein. If you get it right this time your reward is a new account and no further embarrassment.'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)