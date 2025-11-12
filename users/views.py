from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# from django.utils import timezone
import threading

from .models import User, StudentEmail, OTPVerification, StudentProfile, ProfessorEmail
from .forms import EmailVerificationForm, OTPVerificationForm, StudentRegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, CustomUserCreationForm
from datetime import time, timedelta
from django.utils import timezone
from timetable.models import ClassSchedule, Batch

# from django.contrib.auth.decorators import login_required, user_passes_test
# from .models import ProfessorEmail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

def email_verification(request):
    """Step 1: Verify email is in whitelist"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['registration_email'] = email
            
            # Send OTP
            send_otp_email(email)
            messages.success(request, f"OTP sent to {email}")
            return redirect('otp_verification')
    else:
        form = EmailVerificationForm()
    
    return render(request, 'users/email_verification.html', {'form': form})

def otp_verification(request):
    """Step 2: Verify OTP"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    email = request.session.get('registration_email')
    if not email:
        messages.error(request, "Please enter your email first.")
        return redirect('email_verification')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST, email=email)
        if form.is_valid():
            # Mark OTP as used
            otp = OTPVerification.objects.get(
                email=email,
                otp_code=form.cleaned_data['otp_code']
            )
            otp.is_used = True
            otp.save()
            
            messages.success(request, "Email verified successfully!")
            return redirect('student_registration')
    else:
        form = OTPVerificationForm(email=email)
    
    # Resend OTP
    if request.GET.get('resend') == 'true':
        send_otp_email(email)
        messages.info(request, "New OTP sent to your email.")
        return redirect('otp_verification')
    
    context = {
        'form': form,
        'email': email,
    }
    return render(request, 'users/otp_verification.html', context)

def student_registration(request):
    """Step 3: Student fills their details with pre-filled batch/branch"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    email = request.session.get('registration_email')
    if not email:
        messages.error(request, "Please verify your email first.")
        return redirect('email_verification')
    
    # Ensure OTP verified
    if not OTPVerification.objects.filter(email=email, is_used=True).exists():
        messages.error(request, "Please verify your OTP first.")
        return redirect('otp_verification')
    
    # Try to prefill from StudentEmail table
    try:
        student_email = StudentEmail.objects.get(email=email)
        initial_data = {
            'email': email,
            'batch': student_email.batch,
            'branch': student_email.branch,
            'roll_number': student_email.roll_number,
        }
    except StudentEmail.DoesNotExist:
        student_email = None
        initial_data = {'email': email}
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save(commit=False)
            user.email = email
            user.username = email
            user.role = 'student'
            user.email_verified = True
            user.save()
            
            # Create profile
            StudentProfile.objects.create(
                user=user,
                roll_number=form.cleaned_data.get('roll_number', ''),
                batch=form.cleaned_data.get('batch', ''),
                branch=form.cleaned_data.get('branch', ''),
                section=form.cleaned_data.get('section', '')
            )
            
            # Mark student email as registered if it exists
            if student_email:
                student_email.is_registered = True
                student_email.save()
            
            # ✅ FIXED: specify backend explicitly
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Clear session
            request.session.pop('registration_email', None)
            
            messages.success(request, f"Welcome to CampusConnect, {user.get_full_name()}!")
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm(initial=initial_data)
    
    context = {
        'form': form,
        'email': email,
    }
    return render(request, 'users/student_registration.html', context)


def login_view(request):
    """Unified login for students and professors"""
    if request.user.is_authenticated:
        if request.user.role == 'professor':
            return redirect('professor_dashboard')
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').lower().strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, "Please provide both email and password.")
            return render(request, 'users/login.html')

        try:
            # Get user by email
            user = User.objects.get(email=email)
            authenticated_user = authenticate(request, username=user.username, password=password)

            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, f"Welcome back, {authenticated_user.get_full_name()}!")

                # ✅ Redirect based on role
                if authenticated_user.role == 'professor':
                    return redirect('professor_dashboard')
                elif authenticated_user.role == 'student':
                    return redirect('dashboard')
                else:
                    return redirect('home')

            else:
                messages.error(request, "Invalid password.")

        except User.DoesNotExist:
            messages.error(request, "No account found with this email address.")

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def dashboard(request):
    from datetime import time, timedelta
    from django.utils import timezone
    from timetable.models import ClassSchedule, Batch

    user = request.user
    next_classes = []
    ongoing_class = None
    tomorrow_classes = []

    # ✅ FIXED: correct related name (studentprofile)
    if user.role == 'student' and hasattr(user, 'studentprofile'):
        try:
            now = timezone.localtime(timezone.now())
            current_day = now.strftime('%A').lower()
            current_time = now.time()

            # Simulate 9 AM if it’s too early
            if current_time < time(7, 0, 0):
                current_time = time(9, 0, 0)

            student_profile = user.studentprofile
            student_batches = Batch.objects.filter(
                batch_year=student_profile.batch,
                branch__iexact=student_profile.branch.strip().lower()
            )

            # 🔍 DEBUG — log info
            print(f"[DEBUG] Student: {user.email}")
            print(f"[DEBUG] Batch: {student_profile.batch}, Branch: {student_profile.branch}")
            print(f"[DEBUG] Day: {current_day}, Time: {current_time}")
            print(f"[DEBUG] Matched Batches: {student_batches.count()}")

            # Ongoing class
            ongoing_classes = ClassSchedule.objects.filter(
                batch__in=student_batches,
                time_slot__day=current_day,
                time_slot__start_time__lte=current_time,
                time_slot__end_time__gte=current_time
            )
            if ongoing_classes.exists():
                ongoing_class = ongoing_classes.first()

            # Upcoming classes today
            today_classes = ClassSchedule.objects.filter(
                batch__in=student_batches,
                time_slot__day=current_day,
                time_slot__start_time__gt=current_time
            ).order_by('time_slot__start_time')[:5]

            # Fallback: show all today's if nothing upcoming
            if not today_classes.exists():
                today_classes = ClassSchedule.objects.filter(
                    batch__in=student_batches,
                    time_slot__day=current_day
                ).order_by('time_slot__start_time')[:5]

            # Tomorrow preview
            tomorrow = now + timedelta(days=1)
            tomorrow_day = tomorrow.strftime('%A').lower()
            tomorrow_classes = ClassSchedule.objects.filter(
                batch__in=student_batches,
                time_slot__day=tomorrow_day
            ).order_by('time_slot__start_time')[:3]

            next_classes = today_classes

            print(f"[DEBUG] Classes Found: {next_classes.count()}")

        except Exception as e:
            print(f"[ERROR in dashboard]: {e}")

    context = {
        'user': user,
        'next_classes': next_classes,
        'ongoing_class': ongoing_class,
        'tomorrow_classes': tomorrow_classes,
        'current_time': timezone.localtime(timezone.now()),
    }
    return render(request, 'users/dashboard.html', context)


# Email functions
def send_otp_email(email):
    """Send OTP to email"""
    # Delete existing OTPs
    OTPVerification.objects.filter(email=email).delete()

    # Create a new OTP
    otp = OTPVerification.objects.create(email=email)

    # Send email asynchronously
    thread = threading.Thread(target=send_otp_email_async, args=(email, otp.otp_code))
    thread.start()

    print(f"✅ OTP sent to {email}")


def send_otp_email_async(email, otp_code):
    """Actually send the OTP email"""
    subject = 'Your CampusConnect Verification OTP'
    message = f'''
    Hello,

    Your OTP for CampusConnect registration is: {otp_code}

    This OTP will expire in 10 minutes.

    If you didn't request this OTP, please ignore this email.

    Best regards,
    CampusConnect Team
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

def forgot_password(request):
    """Step 1: Request password reset by email"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['reset_email'] = email
            
            # Send OTP for password reset
            send_otp_email(email)
            messages.success(request, f"Password reset OTP sent to {email}")
            return redirect('reset_password_otp')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'users/forgot_password.html', {'form': form})

def reset_password_otp(request):
    """Step 2: Verify OTP for password reset"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, "Please enter your email first.")
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST, email=email)
        if form.is_valid():
            # Mark OTP as used
            otp = OTPVerification.objects.get(
                email=email,
                otp_code=form.cleaned_data['otp_code']
            )
            otp.is_used = True
            otp.save()
            
            messages.success(request, "OTP verified successfully!")
            return redirect('reset_password')
    else:
        form = OTPVerificationForm(email=email)
    
    # Resend OTP
    if request.GET.get('resend') == 'true':
        send_otp_email(email)
        messages.info(request, "New OTP sent to your email.")
        return redirect('reset_password_otp')
    
    context = {
        'form': form,
        'email': email,
    }
    return render(request, 'users/reset_password_otp.html', context)

def reset_password(request):
    """Step 3: Set new password"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, "Please verify your email first.")
        return redirect('forgot_password')
    
    # Verify that OTP was used
    if not OTPVerification.objects.filter(email=email, is_used=True).exists():
        messages.error(request, "Please verify your OTP first.")
        return redirect('reset_password_otp')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            # Get user and set new password
            try:
                user = User.objects.get(email=email)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                
                # Clear session data
                request.session.pop('reset_email', None)
                
                messages.success(request, "Password reset successfully! Please login with your new password.")
                return redirect('login')
                
            except User.DoesNotExist:
                messages.error(request, "User not found. Please try again.")
                return redirect('forgot_password')
    else:
        form = ResetPasswordForm()
    
    context = {
        'form': form,
        'email': email,
    }
    return render(request, 'users/reset_password.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import ProfessorEmail


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, f"Welcome {user.first_name}! Registration successful.")
            if user.role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('professor_dashboard')
    else:
        form = CustomUserCreationForm()

    professor_email_count = ProfessorEmail.objects.count()
    return render(request, 'users/register.html', {
        'form': form,
        'professor_email_count': professor_email_count
    })






def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def manage_professor_emails(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            ProfessorEmail.objects.get_or_create(email=email)
            messages.success(request, f"Added professor email: {email}")
    
    emails = ProfessorEmail.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(emails, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_emails': emails.count(),
    }
    return render(request, 'users/manage_professor_emails.html', context)

@login_required
@user_passes_test(is_admin)
def delete_professor_email(request, email_id):
    email = get_object_or_404(ProfessorEmail, id=email_id)
    if request.method == 'POST':
        email_address = email.email
        email.delete()
        messages.success(request, f"Deleted professor email: {email_address}")
        return redirect('manage_professor_emails')
    
    context = {'email': email}
    return render(request, 'users/delete_professor_email.html', context)


# In users/views.py
def register_staff(request):
    """Staff-specific registration that pre-sets the role"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Staff registration successful!")
            return redirect('professor_dashboard')
    else:
        # Pre-set role to professor
        form = CustomUserCreationForm(initial={'role': 'professor'})
    
    context = {
        'form': form,
        'is_staff_registration': True,
        'professor_email_count': ProfessorEmail.objects.count(),
    }
    return render(request, 'users/register.html', context)