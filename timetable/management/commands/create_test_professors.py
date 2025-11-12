# timetable/management/commands/create_test_professors.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create test professor accounts for development'

    def handle(self, *args, **options):
        User = get_user_model()
        
        professors = [
            {'username': 'prof1', 'email': 'prof1@iiitdmj.ac.in', 'password': 'prof123', 'first_name': 'Amit', 'last_name': 'Sharma'},
            {'username': 'prof2', 'email': 'prof2@iiitdmj.ac.in', 'password': 'prof123', 'first_name': 'Priya', 'last_name': 'Singh'},
            {'username': 'prof3', 'email': 'prof3@iiitdmj.ac.in', 'password': 'prof123', 'first_name': 'Raj', 'last_name': 'Kumar'},
            {'username': 'prof4', 'email': 'prof4@iiitdmj.ac.in', 'password': 'prof123', 'first_name': 'Sunita', 'last_name': 'Verma'},
            {'username': 'prof5', 'email': 'prof5@iiitdmj.ac.in', 'password': 'prof123', 'first_name': 'Anil', 'last_name': 'Gupta'},
        ]

        for prof in professors:
            if not User.objects.filter(email=prof['email']).exists():
                user = User.objects.create_user(
                    username=prof['username'],
                    email=prof['email'], 
                    password=prof['password'],
                    first_name=prof['first_name'],
                    last_name=prof['last_name'],
                    role='professor'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created professor: {prof["email"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Already exists: {prof["email"]}')
                )

        self.stdout.write(
            self.style.SUCCESS('🎉 Successfully created test professors!')
        )
        self.stdout.write('📧 Emails: prof1@iiitdmj.ac.in to prof5@iiitdmj.ac.in')
        self.stdout.write('🔑 Password: prof123')