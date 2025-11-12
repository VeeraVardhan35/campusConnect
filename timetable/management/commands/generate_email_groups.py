from django.core.management.base import BaseCommand
from users.models import EmailGroup, StudentEmail

class Command(BaseCommand):
    help = 'Generate batch and branch email groups'

    def handle(self, *args, **options):
        # Get all unique batches from student emails
        batches = StudentEmail.objects.exclude(batch='').values_list('batch', flat=True).distinct()
        branches = ['cs', 'ec', 'me', 'sm']
        
        created_count = 0
        updated_count = 0
        
        self.stdout.write("Generating email groups...")
        self.stdout.write("=" * 50)
        
        # Create batch groups (btech2023@iiitdmj.ac.in)
        for batch in sorted(batches):
            batch_email = f"btech{batch}@iiitdmj.ac.in"
            batch_name = f"B.Tech {batch} Batch"
            
            group, created = EmailGroup.objects.get_or_create(
                email=batch_email,
                defaults={
                    'name': batch_name,
                    'group_type': 'batch',
                    'batch': batch,
                    'description': f'All B.Tech {batch} students'
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created batch group: {batch_name} <{batch_email}>")
                )
                created_count += 1
            else:
                if group.name != batch_name or group.batch != batch:
                    group.name = batch_name
                    group.batch = batch
                    group.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f"Updated batch group: {batch_name}")
                    )
        
        # Create branch groups (cs2023@iiitdmj.ac.in, etc.)
        for batch in sorted(batches):
            for branch in branches:
                # Check if this branch exists for this batch
                if StudentEmail.objects.filter(batch=batch, branch=branch).exists():
                    branch_email = f"{branch}{batch}@iiitdmj.ac.in"
                    branch_name = f"{branch.upper()} {batch} Branch"
                    
                    group, created = EmailGroup.objects.get_or_create(
                        email=branch_email,
                        defaults={
                            'name': branch_name,
                            'group_type': 'branch',
                            'batch': batch,
                            'branch': branch,
                            'description': f'All {branch.upper()} branch students of {batch} batch'
                        }
                    )
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f"Created branch group: {branch_name} <{branch_email}>")
                        )
                        created_count += 1
                    else:
                        if (group.name != branch_name or group.batch != batch or 
                            group.branch != branch):
                            group.name = branch_name
                            group.batch = batch
                            group.branch = branch
                            group.save()
                            updated_count += 1
                            self.stdout.write(
                                self.style.WARNING(f"Updated branch group: {branch_name}")
                            )
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(
            self.style.SUCCESS(f"Email groups generation complete!")
        )
        self.stdout.write(f"Created: {created_count} new groups")
        self.stdout.write(f"Updated: {updated_count} existing groups")
        self.stdout.write(f"Total groups: {EmailGroup.objects.count()}")
        
        # Show some examples
        self.stdout.write("\nExamples:")
        batch_example = EmailGroup.objects.filter(group_type='batch').first()
        branch_example = EmailGroup.objects.filter(group_type='branch').first()
        
        if batch_example:
            self.stdout.write(f"  Batch: {batch_example.name} <{batch_example.email}>")
        if branch_example:
            self.stdout.write(f"  Branch: {branch_example.name} <{branch_example.email}>")