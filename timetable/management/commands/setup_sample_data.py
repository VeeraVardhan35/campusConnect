from django.core.management.base import BaseCommand
from users.models import User, Department, Batch, StudentProfile, ProfessorProfile
from timetable.models import Course, Classroom, TimeSlot, ClassSchedule
from datetime import time

class Command(BaseCommand):
    help = 'Setup sample data for CampusConnect'

    def handle(self, *args, **options):
        self.stdout.write('Setting up sample data...')
        
        # Create Department
        cs_dept, created = Department.objects.get_or_create(
            name="Computer Science",
            code="CS"
        )
        
        # Create Batch
        cs_batch, created = Batch.objects.get_or_create(
            name="CS-3A",
            department=cs_dept,
            year=3
        )
        
        # Create Professor
        prof_user, created = User.objects.get_or_create(
            username='prof_sharma',
            defaults={
                'first_name': 'Rajesh',
                'last_name': 'Sharma',
                'email': 'sharma@college.edu',
                'role': 'professor'
            }
        )
        prof_user.set_password('prof123')
        prof_user.save()
        
        ProfessorProfile.objects.get_or_create(
            user=prof_user,
            employee_id='PROF001',
            department=cs_dept
        )
        
        # Create Student
        student_user, created = User.objects.get_or_create(
            username='student001',
            defaults={
                'first_name': 'Rahul',
                'last_name': 'Verma',
                'email': 'rahul@student.college.edu',
                'role': 'student'
            }
        )
        student_user.set_password('student123')
        student_user.save()
        
        StudentProfile.objects.get_or_create(
            user=student_user,
            roll_number='CS2023001',
            batch=cs_batch
        )
        
        # Create Courses
        ds_course, created = Course.objects.get_or_create(
            code='CS301',
            name='Data Structures',
            credits=4,
            department=cs_dept
        )
        
        algo_course, created = Course.objects.get_or_create(
            code='CS302',
            name='Algorithms',
            credits=4,
            department=cs_dept
        )
        
        # Create Classrooms
        room301, created = Classroom.objects.get_or_create(
            room_number='301',
            building='Main Building',
            capacity=60
        )
        
        room302, created = Classroom.objects.get_or_create(
            room_number='302', 
            building='Main Building',
            capacity=45
        )
        
        # Create Time Slots
        time_slots = [
            ('09:00', '10:00', 'monday'),
            ('10:00', '11:00', 'monday'),
            ('09:00', '10:00', 'tuesday'),
            ('10:00', '11:00', 'tuesday'),
        ]
        
        for start, end, day in time_slots:
            TimeSlot.objects.get_or_create(
                start_time=start,
                end_time=end,
                day=day
            )
        
        # Create Class Schedules
        m9_slot = TimeSlot.objects.get(day='monday', start_time='09:00')
        m10_slot = TimeSlot.objects.get(day='monday', start_time='10:00')
        
        ClassSchedule.objects.get_or_create(
            course=ds_course,
            professor=prof_user,
            batch=cs_batch,
            classroom=room301,
            time_slot=m9_slot
        )
        
        ClassSchedule.objects.get_or_create(
            course=algo_course,
            professor=prof_user,
            batch=cs_batch,
            classroom=room302,
            time_slot=m10_slot
        )
        
        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )
        self.stdout.write('Test credentials:')
        self.stdout.write('Professor - username: prof_sharma, password: prof123')
        self.stdout.write('Student - username: student001, password: student123')