from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from .models import newUser
from django.contrib.auth import authenticate,login ,logout 
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
# Research about am.

# Create your views here.
def home(request):
    return render(request, 'home.html')

class CreateUserView(View):
    template_name="register.html"
    
    def get(self,request,*args, **kwargs):
        return render(request,self.template_name)
    
    def post(self,request,*args, **kwargs):
        user_name=request.POST.get('user_name')
        email=request.POST.get('email')
        password=request.POST.get("password")
        repeat_password=request.POST.get("repeat_password")
        
        if password != repeat_password:
            messages.add_message(request, messages.ERROR,
                                 "Passwords do not match.")
            return redirect("event:home")
        else:
            user = newUser.objects.create(
                email=email,
                user_name=user_name
            )
            user.set_password(password)
            user.save()
        return redirect("event:home")

@method_decorator(csrf_protect, name='dispatch')   
class LoginView(View):
        template_name="login.html"
        
        def get(self,request,*args,**kwargs):
            return render(request,self.template_name)
        
        def post(self,request,*args,**kwargs):
            email=request.POST.get('email')
            password=request.POST.get('password')
            
            user=authenticate(email=email,password=password)
            
            if user:
                login(request,user)
                return redirect('event:home')
            else:
                messages.add_message(request, messages.ERROR,
                                "Invalid credentials")
                return render(request,self.template_name)
        
    
