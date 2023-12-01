from django import forms
from event.models import Event,EventCategory


class EventForm(forms.ModelForm):


    class Meta:
        model = Event
        fields = ['category', 'title', 'uid', 'description','venue', 'start_date', 'end_date', 'location','maximum_attendance', 'image','status','speaker_name','start_time','end_time']
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
            # 'category': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'category': forms.Select(attrs={'class': 'form-control custom-select'}),
            'status': forms.Select(attrs={'class': 'form-control custom-select'})
        }
        
class CategoryForm(forms.ModelForm):


    class Meta:
        model = EventCategory
        fields = ['name','code']
        # widgets = {
        #     'start_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        #     'end_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        # }





