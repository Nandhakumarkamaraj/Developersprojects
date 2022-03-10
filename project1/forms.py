from django import forms
from django.forms import ModelForm
from .models import Project, Review
from django import forms



class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','image','demo_link','source_link','tags']

        widgets = {
            'tags' : forms.CheckboxSelectMultiple(),
        } 

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for label,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        
        fields = ['value','body']   
        labels = { 'value':'enter a value',
                    'body': 'enter the description',
                }  

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for label,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})           