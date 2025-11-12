from django.core.management.base import BaseCommand
from django.core.management import call_command
from users.models import StudentEmail

class Command(BaseCommand):
    help = 'Generate all student emails and email groups for batches 22,23,24,25'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what emails would be created without actually creating them'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Define the email patterns and ranges
        email_config = {
            'batches': ['22', '23', '24', '25'],
            'branches': {
                'cs': 300,  # CS up to 300
                'ec': 200,  # EC up to 200  
                'me': 80,   # ME up to 80
                'sm': 80    # SM up to 80
            }
        }
        
        total_emails = 0
        created_count = 0
        existing_count = 0
        
        self.stdout.write("Generating student emails...")
        self.stdout.write("=" * 50)
        
        for batch in email_config['batches']:
            self.stdout.write(f"\nProcessing Batch 20{batch}:")
            self.stdout.write("-" * 30)
            
            for branch, max_roll in email_config['branches'].items():
                branch_count = 0
                self.stdout.write(f"  {branch.upper()} branch (rolls 1-{max_roll}):")
                
                for roll in range(1, max_roll + 1):
                    # Format roll number with leading zeros (001, 002, ..., 300)
                    roll_str = f"{roll:03d}"
                    
                    # Create email in format: 23bcs101@iiitdmj.ac.in
                    email = f"{batch}b{branch}{roll_str}@iiitdmj.ac.in"
                    
                    total_emails += 1
                    
                    if dry_run:
                        self.stdout.write(f"    [DRY RUN] Would create: {email}")
                        branch_count += 1
                    else:
                        # Check if email already exists
                        if StudentEmail.objects.filter(email=email).exists():
                            existing_count += 1
                            branch_count += 1
                            continue
                        
                        # Create the student email (auto-extracts batch/branch info)
                        student_email = StudentEmail.objects.create(email=email)
                        created_count += 1
                        branch_count += 1
                
                self.stdout.write(f"    → Generated {branch_count} emails for {branch.upper()}")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("STUDENT EMAILS SUMMARY:")
        self.stdout.write(f"Total emails to generate: {total_emails}")
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f"DRY RUN: Would create {total_emails} emails")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Created {created_count} new student emails")
            )
            self.stdout.write(
                self.style.WARNING(f"Skipped {existing_count} existing student emails")
            )
            
            # Now generate email groups
            self.stdout.write("\n" + "=" * 50)
            self.stdout.write("GENERATING EMAIL GROUPS...")
            call_command('generate_email_groups')
            
            # Show examples
            self.stdout.write("\nEXAMPLES:")
            from users.models import EmailGroup
            batch_groups = EmailGroup.objects.filter(group_type='batch')[:3]
            branch_groups = EmailGroup.objects.filter(group_type='branch')[:3]
            
            self.stdout.write("Batch Groups:")
            for group in batch_groups:
                self.stdout.write(f"  {group.name} <{group.email}>")
            
            self.stdout.write("Branch Groups:")
            for group in branch_groups:
                self.stdout.write(f"  {group.name} <{group.email}>")