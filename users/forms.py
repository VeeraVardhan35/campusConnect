from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import (
    User,
    StudentEmail,
    OTPVerification,
    StudentProfile,
    ProfessorEmail,
)

# ----------------------------
# EMAIL VERIFICATION FORM
# ----------------------------
class EmailVerificationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your college email address",
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()

        try:
            student_email = StudentEmail.objects.get(email=email)
            if student_email.is_registered:
                raise ValidationError(
                    "This email is already registered. Please login instead."
                )
        except StudentEmail.DoesNotExist:
            raise ValidationError(
                "This email is not authorized for registration. Please use your college-provided email."
            )

        return email


# ----------------------------
# OTP VERIFICATION FORM
# ----------------------------
class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter 6-digit OTP"}
        ),
    )

    def __init__(self, *args, **kwargs):
        self.email = kwargs.pop("email", None)
        super().__init__(*args, **kwargs)

    def clean_otp_code(self):
        otp_code = self.cleaned_data.get("otp_code")

        if not otp_code or len(otp_code) != 6 or not otp_code.isdigit():
            raise ValidationError("Please enter a valid 6-digit OTP code")

        try:
            otp = OTPVerification.objects.get(
                email=self.email, otp_code=otp_code, is_used=False
            )
            if not otp.is_valid():
                raise ValidationError("OTP has expired. Please request a new one.")
        except OTPVerification.DoesNotExist:
            raise ValidationError("Invalid OTP code. Please check and try again.")

        return otp_code


# ----------------------------
# STUDENT REGISTRATION FORM
# ----------------------------
class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your first name"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your last name"}
        ),
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your phone number (optional)",
            }
        ),
    )
    roll_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your roll number"}
        ),
    )
    batch = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g., 2023, 2024"}
        ),
    )
    branch = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Select your branch"),
            ("cs", "Computer Science"),
            ("ec", "Electronics & Communication"),
            ("me", "Mechanical Engineering"),
            ("sm", "Smart Manufacturing"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    section = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Select your section"),
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "roll_number",
            "batch",
            "branch",
            "section",
            "password1",
            "password2",
        )
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "readonly": "readonly",
                    "placeholder": "Your college email",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Create a password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm your password"}
        )


# ----------------------------
# LOGIN & PASSWORD FORMS
# ----------------------------
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your registered email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your password"}
        )
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your registered email address",
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()

        try:
            user = User.objects.get(email=email)
            if not user.email_verified:
                raise ValidationError(
                    "This email is not verified. Please contact support."
                )
        except User.DoesNotExist:
            raise ValidationError("No account found with this email address.")

        return email


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter new password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm new password"}
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Passwords don't match")
        return cleaned_data


# ----------------------------
# CUSTOM USER CREATION FORM (Professor + Student)
# ----------------------------
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, ProfessorEmail


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, StudentProfile, ProfessorEmail, StudentEmail


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('professor', 'Professor'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    batch = forms.CharField(max_length=10, required=False)
    branch = forms.ChoiceField(
        choices=[
            ('', 'Select your branch'),
            ('cs', 'Computer Science'),
            ('ec', 'Electronics & Communication'),
            ('me', 'Mechanical Engineering'),
            ('sm', 'Smart Manufacturing'),
        ],
        required=False,
    )
    section = forms.CharField(max_length=1, required=False)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'role', 'password1', 'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()

        if not email:
            raise ValidationError("Email is required.")

        # ✅ Check if email exists in StudentEmail or ProfessorEmail
        is_student = StudentEmail.objects.filter(email__iexact=email).exists()
        is_professor = ProfessorEmail.objects.filter(email__iexact=email).exists()

        if not is_student and not is_professor:
            raise ValidationError(
                "This email is not authorized for registration. "
                "Please use your college-provided email."
            )

        # ✅ Check for duplicates in user table
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already registered.")

        return email

    def clean(self):
        cleaned_data = super().clean()
        email = (cleaned_data.get('email') or '').strip().lower()
        role = cleaned_data.get('role')

        # ✅ Check which list the email is in
        is_student = StudentEmail.objects.filter(email__iexact=email).exists()
        is_professor = ProfessorEmail.objects.filter(email__iexact=email).exists()

        # Enforce correct mapping
        if is_student and role != 'student':
            self.add_error('role', "This email belongs to a student. Please select 'Student'.")
        elif is_professor and role != 'professor':
            self.add_error('role', "This email belongs to a professor. Please select 'Professor'.")

        # Validate student fields if needed
        if role == 'student':
            if not cleaned_data.get('batch'):
                self.add_error('batch', "Batch is required for student registration.")
            if not cleaned_data.get('branch'):
                self.add_error('branch', "Branch is required for student registration.")
            if not cleaned_data.get('section'):
                self.add_error('section', "Section is required for student registration.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
            if user.role == 'student':
                StudentProfile.objects.create(
                    user=user,
                    batch=self.cleaned_data.get('batch', ''),
                    branch=self.cleaned_data.get('branch', ''),
                    section=self.cleaned_data.get('section', '')
                )
        return user
