from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Registration flow
    path('register/', views.email_verification, name='email_verification'),
    path('verify-otp/', views.otp_verification, name='otp_verification'),
    path('complete-registration/', views.student_registration, name='student_registration'),
    
    # Password reset flow
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password-otp/', views.reset_password_otp, name='reset_password_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('register/', views.register, name='register'),
    path('admin/professor-emails/', views.manage_professor_emails, name='manage_professor_emails'),
    path('admin/professor-emails/delete/<int:email_id>/', views.delete_professor_email, name='delete_professor_email'),
]