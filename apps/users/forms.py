from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'required':'true'}))
    password = forms.PasswordField(required=True,widget=forms.PasswordInput(attrs={'required':'true'}))
