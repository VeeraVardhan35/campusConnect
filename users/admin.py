from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentEmail, EmailGroup, OTPVerification, StudentProfile, ProfessorEmail

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'email_verified', 'is_staff')
    list_filter = ('role', 'is_staff', 'email_verified')
    fieldsets = UserAdmin.fieldsets + (
        ('College Info', {'fields': ('role', 'phone', 'email_verified')}),
    )

@admin.register(StudentEmail)
class StudentEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'batch', 'branch', 'roll_number', 'is_registered', 'created_at')
    list_filter = ('batch', 'branch', 'is_registered', 'created_at')
    search_fields = ('email', 'roll_number', 'batch', 'branch')
    readonly_fields = ('batch', 'branch', 'roll_number')
    actions = ['extract_info', 'mark_as_unregistered']

    def extract_info(self, request, queryset):
        for student_email in queryset:
            student_email.extract_info_from_email()
            student_email.save()
        self.message_user(request, f"Extracted info for {queryset.count()} emails.")
    extract_info.short_description = "Extract batch/branch info from emails"

    def mark_as_unregistered(self, request, queryset):
        queryset.update(is_registered=False)
    mark_as_unregistered.short_description = "Mark selected emails as unregistered"

@admin.register(EmailGroup)
class EmailGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'group_type', 'batch', 'branch', 'is_active')
    list_filter = ('group_type', 'batch', 'branch', 'is_active')
    search_fields = ('name', 'email', 'batch', 'branch')
    actions = ['generate_group_emails']

    def generate_group_emails(self, request, queryset):
        from timetable.management.commands.generate_email_groups import Command
        command = Command()
        command.handle()
        self.message_user(request, "Generated all email groups.")
    generate_group_emails.short_description = "Generate batch and branch email groups"

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp_code', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('email', 'otp_code')
    readonly_fields = ('created_at', 'expires_at')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'batch', 'branch')
    search_fields = ('user__first_name', 'user__last_name', 'roll_number', 'batch', 'branch')
    list_filter = ('batch', 'branch')


# from django.contrib import admin
# from .models import ProfessorEmail

@admin.register(ProfessorEmail)
class ProfessorEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']
    search_fields = ['email']
    list_filter = ['created_at']


admin.site.register(User, CustomUserAdmin)