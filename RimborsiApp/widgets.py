from django import forms
import os
from django.conf import settings


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'django/forms/widgets/custom_clearable_file_input.html'


class PastiCustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'django/forms/widgets/custom_clearable_file_input2.html'


class FirmeCustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'django/forms/widgets/custom_clearable_file_input3.html'