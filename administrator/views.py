from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from event.models import newUser
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your models here.

class HomeView(LoginRequiredMixin,View):
    template_name="dashboard/index.html"
    
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
    
class CreateAdminView(View):
    template_name = "dashboard/accounts/create_administrator.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('repeat_password')
        
        if password != confirm_password:
            messages.add_message(request, messages.ERROR, "Passwords do not match")
            return redirect("administrator:create_admin")
        
        elif newUser.objects.filter(email=email).exists() or newUser.objects.filter(user_name=username).exists():
            messages.add_message(request, messages.ERROR, "User already exists")
            return redirect("administrator:create_admin")
        
        else:
            user = newUser.objects.create(
                email=email,
                user_name=username
            )
            user.set_password(password)
            user.is_active = True
            user.is_staff = True  # Consider if this is appropriate for your use case
            user.save()
            
        return redirect("administrator:dash_home")
    
class LoginView(View):
    template_name="dashboard/accounts/login.html"
            
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
    
    def post(self,request,*args,**kwargs):
            email=request.POST.get('email')
            password=request.POST.get('password')
            
            user=authenticate(email=email,password=password)
            
            if user is not None and user.is_staff:
                login(request,user)
                return redirect("administrator:dash_home")    
            
            else:
                messages.add_message(request,messages.ERROR,"Invalid login from anonymous user")
                return redirect("administrator:login")
                
            
                
        

            
              
        
