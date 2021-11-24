from django.forms import ModelForm, fields
from .models import Step

class StepForm(ModelForm):
  class Meta:
    model = Step
    fields = ["date", "step"]