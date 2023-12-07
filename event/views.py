from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib import messages
from .models import newUser,Event, RegisteredUser
from django.contrib.auth import authenticate,login ,logout 
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

# Research about am.

# Create your views here.
def home(request):
    return render(request, 'home.html')

class HomeView(LoginRequiredMixin,View):
    template_name="index.html"
    login_url = "event:login" 
    
    def get(self,request,*args,**kwargs):
        events=Event.objects.all()
        context={"event":events}
        return render(request,self.template_name,context)
    
class EventDetailsView(View):
    template_name="event-details.html"
    def get(self,request,event_id,*args,**kwargs):
        event=get_object_or_404(Event,id=event_id)
        context={"event":event}
        return render(request,self.template_name,context)


class RegisterEventView(View):
    
    template_name = "register_event.html"

    def get(self, request, event_id, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, event_id, *args, **kwargs):
        user_email = request.POST.get('email')
        event = Event.objects.get(pk=event_id)

        try:
            # Check if the user is already registered for the event
            if user_email == request.user.email:
                existing_registration = RegisteredUser.objects.get(event=event, email=user_email)
                return HttpResponseServerError("You are already registered for this event.")
            
            else:
                messages.add_message(request,messages.ERROR,"Invalid User")
                return redirect("event:register_event")
                
                
                

        except RegisteredUser.DoesNotExist:
            # If the user is not already registered, proceed with registration
            user, created = newUser.objects.get_or_create(email=user_email)

            # Generate a registration code (you might want to use a more sophisticated method)
            registration_code = default_token_generator.make_token(user)
            registration_code = urlsafe_base64_encode(force_bytes(registration_code))

            # Save the user registration
            RegisteredUser.objects.create(event=event, email=user_email, registration_code=registration_code)

            # Send email
            send_mail(
                'Event Registration',
                f'Thank you for registering for the event. Your registration code is: {registration_code}',
                'yawsarfo2019@gmail.com',  # Replace with your email sender address
                [user_email],
                fail_silently=False,
            )

            # Pass additional context directly
            context = {
                'user_email': user_email,
                'registration_code': registration_code,
            }

            return render(request, self.template_name, context)


        
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
 
# class LoginView(View):
#     template_name = "login.html"

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         user = authenticate(email=email, password=password)

#         if user:
#             print("User authenticated:", user)
#             login(request, user)
#             return redirect('event:home')
#         else:
#             print("Invalid credentials. Email:", email)
#             messages.add_message(request, messages.ERROR, "Invalid credentials")
#             return render(request, self.template_name)

            
from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib import messages

class LoginView(View):
    template_name="login.html"
            
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
    
    def post(self,request,*args,**kwargs):
            email=request.POST.get('email')
            password=request.POST.get('password')
            
            user=authenticate(email=email,password=password)
            
            if user is not None:
                login(request,user)
                return redirect("event:home")    
            
            else:
                messages.add_message(request,messages.ERROR,"Invalid login from anonymous user")
                return redirect("event:login")



            
            
            
            
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('event:home')
        
    
