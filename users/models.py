from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random
import string
import re

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    email_verified = models.BooleanField(default=False)
    short_name = models.CharField(max_length=10, blank=True, null=True)  # Only for professors

    def save(self, *args, **kwargs):
        # Clear short_name if user is not a professor
        if self.role != 'professor' and self.short_name:
            self.short_name = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

class StudentEmail(models.Model):
    """Whitelist of allowed student emails with auto-extracted info"""
    email = models.EmailField(unique=True)
    is_registered = models.BooleanField(default=False)
    batch = models.CharField(max_length=10, blank=True)
    branch = models.CharField(max_length=10, blank=True)
    roll_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.email and not (self.batch and self.branch):
            self.extract_info_from_email()
        super().save(*args, **kwargs)

    def extract_info_from_email(self):
        """Extract batch, branch, and roll number from email pattern like 23bsm037@iiitdmj.ac.in"""
        pattern = r'(\d{2})(b)?(cs|ec|me|sm)(\d+)@iiitdmj\.ac\.in'
        match = re.match(pattern, self.email.lower())
        
        if match:
            year, b_prefix, branch_code, roll = match.groups()
            self.batch = f"20{year}"
            self.branch = branch_code
            self.roll_number = roll

    def __str__(self):
        info = []
        if self.batch:
            info.append(f"Batch: {self.batch}")
        if self.branch:
            info.append(f"Branch: {self.branch}")
        if self.roll_number:
            info.append(f"Roll: {self.roll_number}")
        
        info_str = f" ({', '.join(info)})" if info else ""
        return f"{self.email}{info_str}"

class EmailGroup(models.Model):
    """Model to manage batch and branch group emails"""
    GROUP_TYPE_CHOICES = (
        ('batch', 'Batch'),
        ('branch', 'Branch'),
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    group_type = models.CharField(max_length=10, choices=GROUP_TYPE_CHOICES)
    batch = models.CharField(max_length=10, blank=True)
    branch = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['group_type', 'batch', 'branch']
    
    def __str__(self):
        return f"{self.name} <{self.email}>"
    
    def get_student_emails(self):
        """Get all student emails that belong to this group"""
        if self.group_type == 'batch':
            return StudentEmail.objects.filter(batch=self.batch)
        elif self.group_type == 'branch':
            return StudentEmail.objects.filter(batch=self.batch, branch=self.branch)
        return StudentEmail.objects.none()

class OTPVerification(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.otp_code:
            self.otp_code = self.generate_otp()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def generate_otp(self):
        return ''.join(random.choices(string.digits, k=6))

    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expires_at

    def __str__(self):
        return f"{self.email} - {self.otp_code}"

class StudentProfile(models.Model):
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
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, blank=True)
    batch = models.CharField(max_length=10, blank=True)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, blank=True)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES, blank=True)

    def __str__(self):
        info = []
        if self.roll_number:
            info.append(f"Roll: {self.roll_number}")
        if self.batch:
            info.append(f"Batch: {self.batch}")
        if self.branch:
            branch_display = dict(self.BRANCH_CHOICES).get(self.branch, self.branch).upper()
            info.append(f"Branch: {branch_display}")
        if self.section:
            info.append(f"Section: {self.section}")
        
        info_str = f" ({', '.join(info)})" if info else ""
        return f"{self.user.get_full_name()}{info_str}"
    

class ProfessorEmail(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Professor Email"
        verbose_name_plural = "Professor Emails"