from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from event.models import newUser,Event
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your models here.
from administrator.forms import EventForm,CategoryForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

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
                        
        
class CreateEventView(View):
    template_name="dashboard/create_event.html"
    
    def get(self,request,*args,**kwargs):
        form=EventForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=EventForm(request.POST,request.FILES)
        
        if form.is_valid():
            event=form.save(commit=False)
            event.save()
            
            messages.success(request, 'Event created successfully!')
            return redirect('administrator:dash_home')
        
        else:
            messages.error(request, 'Invalid form submission. Please check the data entered.')
            return render(request, self.template_name, {'form': form})
        
class CreateCategoryView(View):
    template_name="dashboard/create_event_cat.html"
    
    def get(self,request,*args,**kwargs):
        form=CategoryForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=CategoryForm(request.POST)
        
        if form.is_valid():
            event_category=form.save(commit=False)
            event_category.save()
            
            messages.success(request, 'Event created successfully!')
            return redirect('administrator:dash_home')
        
        else:
            messages.error(request, 'Invalid form submission. Please check the data entered.')
            return render(request, self.template_name, {'form': form})
        
class EventListView(View):
    template_name = "dashboard/event_list.html"
    
    def get(self, request, *args, **kwargs):
        try:
            events = Event.objects.all()
            context = {"event": events}
        except Event.DoesNotExist:
            # Handle the case when no events are found
            context = {"event": None}

        return render(request, self.template_name, context)
    
class EventDetailView(View):
    template_name = "dashboard/event_detail.html"

    def get(self, request, event_id, *args, **kwargs):
        try:
            # Attempt to retrieve the event by its ID
            event = get_object_or_404(Event, id=event_id)
            context = {"event": event}
        except Event.DoesNotExist:
            # Handle the case when no events are found
            context = {"event": None}

        return render(request, self.template_name, context)
    
class EventUpdateView(View):
    template_name = "dashboard/event_update.html"

    def get(self, request, event_id, *args, **kwargs):
        # Retrieve the event by its ID
        event = get_object_or_404(Event, id=event_id)
        form = EventForm(instance=event)
        context = {"event": event, "form": form}
        return render(request, self.template_name, context)

    def post(self, request, event_id, *args, **kwargs):
        # Retrieve the event by its ID
        event = get_object_or_404(Event, id=event_id)
        form = EventForm(request.POST, instance=event)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('administrator:event_detail', args=[event.id]))
        else:
            # Form is not valid, render the template with errors
            context = {"event": event, "form": form}
            return render(request, self.template_name, context)
        
class EventDeleteView(View):
    template_name = "dashboard/event_delete.html"

    def get(self, request, event_id, *args, **kwargs):
        # Retrieve the event by its ID
        event = get_object_or_404(Event, id=event_id)
        context = {"event": event}
        return render(request, self.template_name, context)

    def post(self, request, event_id, *args, **kwargs):
        # Retrieve the event by its ID
        event = get_object_or_404(Event, id=event_id)
        
        # Delete the event
        event.delete()

        return HttpResponseRedirect(reverse('administrator:event_list'))

           
              
        
