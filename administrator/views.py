from django.shortcuts import render
from django.views.generic import View
# Create your models here.

class HomeView(View):
    template_name="dashboard/index.html"
    
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
