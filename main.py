from django.contrib import admin
from core.models import Branch, Dept, Vacancy, Step, City
from django import forms

class StepAdminForm(forms.ModelForm):
    menu = forms.ChoiceField()

    class Meta:
        model = Step
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['menu'].choices = [(f.name, f.name) for f in Vacancy._meta.get_fields()[3:]]

class StepAdmin(admin.ModelAdmin):
    form = StepAdminForm

class VacancyAdminForm(forms.ModelForm):
    list_display = ('title', 'description')
