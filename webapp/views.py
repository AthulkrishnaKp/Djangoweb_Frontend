from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from webapp.models import MyUser,Post
from django.shortcuts import render, redirect
from .forms import SignUpForm,LoginForm,PostForm
from django.views.generic import CreateView,FormView,ListView,View,UpdateView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator




def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)    
    return wrapper

decs=[signin_required,never_cache]


class SignupView(CreateView):
    model=MyUser   
    form_class=SignUpForm
    template_name='signup.html'
    success_message="User has been created"
    success_url=reverse_lazy('signin')

class LoginFormView(FormView):
    form_class=LoginForm
    template_name='login.html'

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)   
        if form.is_valid():
            uname=form.cleaned_data.get("username")   
            pwd=form.cleaned_data.get("password") 
            usr=authenticate(request,username=uname,password=pwd) 
            if usr:
                login(request,usr)
                messages.success(request,"Login Successfull")
                return redirect('home')
            else:
                messages.success(request,"Invalid Credentials")                            
                return render(request,"login.html",{"form":form})

@method_decorator(decs,name="dispatch")
class HomeView(CreateView,ListView):
    model=Post
    form_class=PostForm
    template_name='home.html'
    context_object_name="posts"
    success_url=reverse_lazy("home")
    pk_url_kwarg='id'

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        return context
    

@method_decorator(decs,name="dispatch")    
class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Post.objects.filter(id=id).delete() 
        messages.success(request,"You Deleted one of your Post")    
        return redirect("home")

@method_decorator(decs,name="dispatch")       
class PostUpdateView(UpdateView):
    model=Post
    form_class=PostForm
    template_name="postupdate.html"
    pk_url_kwarg='id'
    success_url=reverse_lazy("home")


decs
def like_post(request,*args,**kwargs):
    p_id=kwargs.get("id")
    p=Post.objects.get(id=p_id)
    p.no_of_likes.add(request.user)
    p.save()
    messages.success(request,"You Liked the post")
    return redirect('home')
    
decs
def unlike_post(request,*args,**kwargs):
    p_id=kwargs.get("id")
    p=Post.objects.get(id=p_id)
    p.no_of_likes.remove(request.user)
    p.save()
    messages.success(request,"You Unliked the Post")
    return redirect('home')    

decs
def signout_view(request,*args,**kwargs):
    logout(request)
    messages.success(request,"User Logged out")
    return redirect("signin")