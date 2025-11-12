# Create a new file: fix_professor_emails.py
from django.core.management.base import BaseCommand
from users.models import ProfessorEmail

class Command(BaseCommand):
    help = 'Fix professor emails with proper domain'

    def handle(self, *args, **options):
        # All professor emails with proper @iiitdmj.ac.in domain
        professor_emails = [
            'anilk@iiitdmj.ac.in', 'pnkondekar@iiitdmj.ac.in', 'dineshk@iiitdmj.ac.in',
            'amresh@iiitdmj.ac.in', 'asish.kundu@iiitdmj.ac.in', 'bhupen@iiitdmj.ac.in',
            'balyan@iiitdmj.ac.in', 'mkpanda@iiitdmj.ac.in', 'mkroy@iiitdmj.ac.in',
            'neeraj@iiitdmj.ac.in', 'nihar@iiitdmj.ac.in', 'nrjena@iiitdmj.ac.in',
            'yashpalk@iiitdmj.ac.in', 'manand@iiitdmj.ac.in', 'jamfareen@iiitdmj.ac.in',
            'amarnath@iiitdmj.ac.in', 'chella@iiitdmj.ac.in', 'himansu@iiitdmj.ac.in',
            'kponappa@iiitdmj.ac.in', 'ptandon@iiitdmj.ac.in', 'shivdayal@iiitdmj.ac.in',
            'sujoy@iiitdmj.ac.in', 'tanush@iiitdmj.ac.in', 'vkgupta@iiitdmj.ac.in',
            'dip.samajdar@iiitdmj.ac.in', 'koushikdutta@iiitdmj.ac.in', 'pankaj.sharma@iiitdmj.ac.in',
            'amitv@iiitdmj.ac.in', 'prabir@iiitdmj.ac.in', 'atul@iiitdmj.ac.in',
            'aojha@iiitdmj.ac.in', 'nitish.andola@iiitdmj.ac.in', 'rakesh.s@iiitdmj.ac.in',
            'deepmala@iiitdmj.ac.in', 'prabin16@iiitdmj.ac.in', 'praikwal@iiitdmj.ac.in',
            'subirs@iiitdmj.ac.in', 'jtiwari@iiitdmj.ac.in', 'sraban@iiitdmj.ac.in',
            'pkhanna@iiitdmj.ac.in', 'ranjeet.kr@iiitdmj.ac.in', 'dsramteke@iiitdmj.ac.in',
            'sa@iiitdmj.ac.in', 'snsharma@iiitdmj.ac.in',
            # Placeholder professors
            'mkt@iiitdmj.ac.in', 'sgm@iiitdmj.ac.in', 'mza@iiitdmj.ac.in', 'arr@iiitdmj.ac.in',
            'shm@iiitdmj.ac.in', 'ds@iiitdmj.ac.in', 'tk@iiitdmj.ac.in', 'chs@iiitdmj.ac.in',
            'ans@iiitdmj.ac.in', 'acp@iiitdmj.ac.in', 'vkj@iiitdmj.ac.in', 'ms@iiitdmj.ac.in',
            'sks@iiitdmj.ac.in', 'as@iiitdmj.ac.in', 'cd@iiitdmj.ac.in', 'vmathur@iiitdmj.ac.in',
            'skchoudhary@iiitdmj.ac.in', 'rpatel@iiitdmj.ac.in'
        ]

        created_count = 0
        updated_count = 0

        self.stdout.write("Updating professor emails...")

        for email in professor_emails:
            # Normalize email
            normalized_email = email.lower().strip()
            
            try:
                obj, created = ProfessorEmail.objects.get_or_create(email=normalized_email)
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"✓ Created: {normalized_email}"))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f"↻ Already exists: {normalized_email}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Error with {normalized_email}: {e}"))

        self.stdout.write(f"\nSummary: {created_count} created, {updated_count} already existed")
        self.stdout.write(f"Total professor emails: {ProfessorEmail.objects.count()}")