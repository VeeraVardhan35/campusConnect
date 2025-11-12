from django.db import models
from users.models import User
import datetime

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Classroom(models.Model):
    room_number = models.CharField(max_length=20, unique=True)
    building = models.CharField(max_length=50, default="Main Building")
    capacity = models.IntegerField(default=60)

    def __str__(self):
        return f"{self.building} - {self.room_number}"

class TimeSlot(models.Model):
    DAY_CHOICES = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    )
    
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=10, choices=DAY_CHOICES)

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.day.title()} {self.start_time}-{self.end_time}"

class Batch(models.Model):
    BRANCH_CHOICES = (
        ('cs', 'Computer Science'),
        ('ec', 'Electronics & Communication'),
        ('me', 'Mechanical Engineering'),
        ('sm', 'Smart Manufacturing'),
    )
    
    SECTION_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    
    name = models.CharField(max_length=50)
    batch_year = models.CharField(max_length=10, blank=True)  # e.g., "2023", "2024"
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, blank=True)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES, blank=True)

    class Meta:
        unique_together = ['batch_year', 'branch', 'section']
        ordering = ['batch_year', 'branch', 'section']

    def save(self, *args, **kwargs):
        # Auto-generate name if not provided
        if not self.name and self.batch_year and self.branch and self.section:
            branch_display = dict(self.BRANCH_CHOICES).get(self.branch, self.branch).upper()
            self.name = f"{branch_display} - Section {self.section} (Batch {self.batch_year})"
        super().save(*args, **kwargs)

    def __str__(self):
        info = []
        if self.batch_year:
            info.append(f"Batch: {self.batch_year}")
        if self.branch:
            branch_display = dict(self.BRANCH_CHOICES).get(self.branch, self.branch).upper()
            info.append(f"Branch: {branch_display}")
        if self.section:
            info.append(f"Section: {self.section}")
        
        info_str = f" ({', '.join(info)})" if info else ""
        return f"{self.name}{info_str}"

class ClassSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'professor'})
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ['classroom', 'time_slot'],
            ['batch', 'time_slot'],
        ]
        ordering = ['time_slot__day', 'time_slot__start_time']

    def __str__(self):
        return f"{self.course.code} - {self.batch.name} - {self.time_slot}"
    

    # In your timetable/models.py, add:

from django.db import models
from users.models import User

class ClassroomBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    professor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'professor'})
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    course_code = models.CharField(max_length=20, blank=True)
    course_name = models.CharField(max_length=200)
    purpose = models.TextField(help_text="Purpose of booking")
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['classroom', 'date', 'start_time', 'end_time']
    
    def __str__(self):
        return f"{self.course_code} - {self.classroom.room_number} on {self.date}"
    
    @property
    def duration(self):
        start = datetime.combine(datetime.min, self.start_time)
        end = datetime.combine(datetime.min, self.end_time)
        return end - start