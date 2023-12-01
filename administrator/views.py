from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from event.models import newUser
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your models here.
from django.shortcuts import get_object_or_404

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
                
            
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('event:home')
    
class ChangePasswordView(LoginRequiredMixin,View):
    template_name="dashboard/accounts/change_password.html"
    def get(self,request,*args,**kwargs):
        administrator=request.user
        context={"administrator":administrator}
        return render(request,self.template_name,context)
    
    def post(self,request,*args,**kwargs):
        current_password=request.POST.get('current_password')
        password=request.POST.get('password')
        repeat_password=request.POST.get('repeat_password')
        admin_id=request.POST.get('admin_id')
        
        user_to_change = get_object_or_404(newUser, id=admin_id)
        loggedin_user=authenticate(email=request.user.email,password=current_password)
        
        if not loggedin_user:
            messages.add_message(request, messages.ERROR,
                                 "Invalid credentials")
        
        elif password != repeat_password:
            messages.add_message(request, messages.ERROR,
                                 "Passwords do not match.")
        
        elif loggedin_user.is_staff or loggedin_user == user_to_change:
            user_to_change.set_password(password)
            user_to_change.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Password updated successfully.")
            
        elif loggedin_user == user_to_change:
            login(request, loggedin_user)
        else:
            messages.add_message(request, messages.ERROR, "Forbidden")
        return redirect(request.META.get("HTTP_REFERER"))
                        
        

            
              
        
