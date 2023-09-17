
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from webapp.models import MyUser,Post


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=MyUser.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'tagging-input'}),
        required=False, 
    )

    class Meta:
        model = Post
        fields = ('title','description','tags')

        widgets={
            "title":forms.Textarea(attrs={"class":"form-control border border-warning mt-2","rows":3,"placeholder":"Title ..."}),
            "description":forms.Textarea(attrs={"class":"form-control border border-warning mt-2","rows":3,"placeholder":"Write a description ..."}),
        }



class SignUpForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-info ","placeholder":"enter password"}))  
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-info","placeholder":"confirm password"}))              
    
   
    class Meta:
        model = MyUser
        fields = ('name', 'email', 'mobile', 'username', 'password1', 'password2')
        
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control border border-info","placeholder":"enter your name"}),
            "mobile":forms.TextInput(attrs={"class":"form-control border border-info","placeholder":"enter mobile number"}),
            "email":forms.EmailInput(attrs={"class":" form-control border border-info","placeholder":"enter email id"}),
        }

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validate_password(password)
        return password


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control border border-info","PlaceHolder":"..."}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-info","PlaceHolder":"..."}))

