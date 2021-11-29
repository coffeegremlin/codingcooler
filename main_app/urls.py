from django.urls import path
from . import views

urlpatterns = [
  # localhost:8000/
  path('', views.Home.as_view(), name='home'),
  # localhost:8000/about/
  path('about/', views.about, name='about'),
  # localhost:8000/projects/
  path('projects/', views.projects_index, name='projects_index'),
  # localhost:8000/projects/:project_id
  path('projects/<int:project_id>/', views.projects_detail, name='projects_detail'),
  # localhost:8000/projects/create
  path('projects/create/', views.ProjectCreate.as_view(), name='projects_create'),
  # localhost:8000/projects/
  path('projects/<int:pk>/update', views.ProjectUpdate.as_view(), name='projects_update'),
  # localhost:8000/projects/:pk/delete
  path('projects/<int:pk>/delete', views.ProjectDelete.as_view(), name='projects_delete'),
  # localhost:8000/projects/:project_id/add_step/
  path('projects/<int:project_id>/add_step/', views.add_step, name='add_step'),

  # path('projects/<int:project_id>/delete_step', views.delete_step, name='delete_step'),
  # localhost:8000/resources/create/
  path('resources/create/', views.ResourceCreate.as_view(), name='resources_create'),
  # localhost:8000/resources/:pk/
  path('resources/<int:pk>/', views.ResourceDetail.as_view(), name='resources_detail'),
  # localhost:8000/resources/
  path('resources/', views.ResourceList.as_view(), name='resources_index'),
  # localhost:8000/resources/:pk/update/
  path('resources/<int:pk>/update/', views.ResourceUpdate.as_view(), name='resources_update'),
  # localhost:8000/resources/:pk/delete/
  path('resources/<int:pk>/delete/', views.ResourceDelete.as_view(), name='resources_delete'),
  # localhost:8000/projects/:project_id/assoc_resource/:resource_id/
  path('projects/<int:project_id>/assoc_resource/<int:resource_id>/', views.assoc_resource, name='assoc_resource'),
  # localhost:8000/projects/project_id/add_wireframe/
  path('projects/<int:project_id>/add_wireframe/', views.add_wireframe, name='add_wireframe'),
  # localhost:8000/accounts/signup/
  path('accounts/signup/', views.signup, name='signup')
]