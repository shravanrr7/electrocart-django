from django import forms
from django.forms import fields, widgets
from .models import Account

class RegisterationForm(forms.ModelForm):
    password =forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'password',
        'class':'form-control'
    }))
    confirm_password =forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Renter password'
    }))
    class Meta:
        model = Account
        fields= ['first_name','last_name','phone_number','email','password']


    def clean(self):
        cleaned_data = super(RegisterationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "password does not match"
                )


    def __init__(self,*args,**kwargs):
        super(RegisterationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


            
        