from django import forms
from .models import ClassroomBooking, Classroom, Batch
from django.utils import timezone
from datetime import datetime, time, date

class ClassroomBookingForm(forms.ModelForm):
    class Meta:
        model = ClassroomBooking
        fields = ['classroom', 'date', 'start_time', 'end_time', 'course_code', 'course_name', 'purpose', 'batch']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'purpose': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.professor = kwargs.pop('professor', None)
        super().__init__(*args, **kwargs)
        
        # Set minimum date to today
        self.fields['date'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%d')
        
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        classroom = cleaned_data.get('classroom')
        
        if date and start_time and end_time:
            if date < timezone.now().date():
                raise forms.ValidationError("Cannot book classrooms for past dates.")
            
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")
            
            # Check if classroom is already booked for this time
            if classroom:
                conflicting_bookings = ClassroomBooking.objects.filter(
                    classroom=classroom,
                    date=date,
                    status__in=['pending', 'approved'],
                    start_time__lt=end_time,
                    end_time__gt=start_time
                )
                
                if self.instance.pk:
                    conflicting_bookings = conflicting_bookings.exclude(pk=self.instance.pk)
                
                if conflicting_bookings.exists():
                    raise forms.ValidationError(
                        f"Classroom {classroom.room_number} is already booked for the selected time."
                    )
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.professor:
            instance.professor = self.professor
        if commit:
            instance.save()
        return instance