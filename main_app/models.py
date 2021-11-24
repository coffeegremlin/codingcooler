from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
COMPLETE = (
  ('Y', 'Yes'),
  ('N', 'No')
)

class Resource(models.Model):
  name = models.CharField(max_length=50)
  url = models.CharField(max_length=200)

  def __str__(self):
    return self.name
  def get_absolute_url(self):
      return reverse("resources_detail", kwargs={"pk": self.id})


class Project(models.Model):
  name = models.CharField(max_length=20)
  programming_language = models.CharField(max_length=20)
  description = models.TextField(max_length=250)
  resources = models.ManyToManyField(Resource)
  # steps = models.ManyToOneRel()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  complete = models.BooleanField

  def __str__(self):
    return self.name

  def get_absolute_url(self):
      return reverse('projects_detail', kwargs={'project_id': self.id})

class Step(models.Model):
  name = models.CharField(max_length=200)
  content = models.TextField(blank=True)
  date = models.DateField('Creation date')
  step = models.CharField(max_length=50)

  class Meta:
    ordering = ['-date']

  def __str__(self):
    return f'{self.get_step_display()} on {self.date}'

  # def updated_today(self):
  #   return self.step_set.filter(date=date.today()).count() >= len()
  # Find a way to show if project was updated today based off if a step was added today

class Wireframe(models.Model):
  url = models.CharField(max_length=250)
  project = models.OneToOneField(Project, on_delete=models.CASCADE)

  def __str__(self):
    return f'Wireframe for the project_id: {self.project_id} @{self.url}'