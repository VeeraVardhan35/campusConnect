from django.contrib import admin
from .models import Course, Classroom, TimeSlot, Batch, ClassSchedule

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'credits')
    search_fields = ('code', 'name')

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'building', 'capacity')
    list_filter = ('building',)
    search_fields = ('room_number',)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time')
    list_filter = ('day',)
    ordering = ('day', 'start_time')

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_year', 'branch', 'section')
    list_filter = ('batch_year', 'branch', 'section')
    search_fields = ('name', 'batch_year', 'branch', 'section')

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'professor', 'batch', 'classroom', 'time_slot')
    list_filter = ('batch__batch_year', 'batch__branch', 'batch__section', 'time_slot__day')
    search_fields = ('course__code', 'course__name', 'professor__first_name')