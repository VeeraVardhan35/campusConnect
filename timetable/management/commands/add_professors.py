from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from users.models import User

class Command(BaseCommand):
    help = 'Add professors to the database with short names'

    def handle(self, *args, **options):
        professors_data = [
            # Format: [Name, ShortName, Email]
            ['Anil Kumar', 'AK', 'anilk@iiitdmj.ac.in'],
            ['P.N. Kondekar', 'PNK', 'pnkondekar@iiitdmj.ac.in'],
            ['Dinesh Kumar V', 'DKV', 'dineshk@iiitdmj.ac.in'],
            ['Amaresh Chandra Mishra', 'ACM', 'amresh@iiitdmj.ac.in'],
            ['Asish K. Kundu', 'AKK', 'asish.kundu@iiitdmj.ac.in'],
            ['Bhupendra Gupta', 'BG', 'bhupen@iiitdmj.ac.in'],
            ['Lokendra Kumar Balyan', 'LKB', 'balyan@iiitdmj.ac.in'],
            ['Manoj Kumar Panda', 'MKP', 'mkpanda@iiitdmj.ac.in'],
            ['Mukesh Kumar Roy', 'MKR', 'mkroy@iiitdmj.ac.in'],
            ['Neeraj K. Jaiswal', 'NKJ', 'neeraj@iiitdmj.ac.in'],
            ['Nihar Kumar Mahato', 'NKM', 'nihar@iiitdmj.ac.in'],
            ['Nihar Ranjan Jena', 'NRJ', 'nrjena@iiitdmj.ac.in'],
            ['Yashpal Singh Katharria', 'YSK', 'yashpalk@iiitdmj.ac.in'],
            ['Mamta Anand', 'MA', 'manand@iiitdmj.ac.in'],
            ['J. Al Muzzamil Fareen', 'JAMF', 'jamfareen@iiitdmj.ac.in'],
            ['Amarnath M.', 'AM', 'amarnath@iiitdmj.ac.in'],
            ['H. Chelladurai', 'HC', 'chella@iiitdmj.ac.in'],
            ['Himansu S. Nanda', 'HSN', 'himansu@iiitdmj.ac.in'],
            ['K. Ponappa', 'KP', 'kponappa@iiitdmj.ac.in'],
            ['Puneet Tandon', 'PT', 'ptandon@iiitdmj.ac.in'],
            ['Shivdayal Patel', 'SP', 'shivdayal@iiitdmj.ac.in'],
            ['Sujoy Mukherjee', 'SM', 'sujoy@iiitdmj.ac.in'],
            ['Tanuja Sheorey', 'TS', 'tanush@iiitdmj.ac.in'],
            ['Vijay Kumar Gupta', 'VKG', 'vkgupta@iiitdmj.ac.in'],
            ['Dip Prakash Samajdar', 'DPS', 'dip.samajdar@iiitdmj.ac.in'],
            ['Koushik Dutta', 'KD', 'koushikdutta@iiitdmj.ac.in'],
            ['Pankaj Sharma', 'PS', 'pankaj.sharma@iiitdmj.ac.in'],
            ['Amit Vishwakarma', 'AV', 'amitv@iiitdmj.ac.in'],
            ['Prabir Mukhopadhyay', 'PM', 'prabir@iiitdmj.ac.in'],
            ['Atul Gupta', 'AG', 'atul@iiitdmj.ac.in'],
            ['Aparajita Ojha', 'AO', 'aojha@iiitdmj.ac.in'],
            ['Nitish Andola', 'NA', 'nitish.andola@iiitdmj.ac.in'],
            ['Rakesh Kumar Sanodiya', 'RKS', 'rakesh.s@iiitdmj.ac.in'],
            ['Deepmala', 'DM', 'deepmala@iiitdmj.ac.in'],
            ['Prabin Kumar Padhy', 'PKP', 'prabin16@iiitdmj.ac.in'],
            ['Pushpa Raikwal', 'PR', 'praikwal@iiitdmj.ac.in'], 
            ['Subir Lamba', 'SSL', 'subirs@iiitdmj.ac.in'],
            ['Jitendar Kumar Tiwari', 'JKT', 'jtiwari@iiitdmj.ac.in'],
            
            # New professors with corrected information
            ['Sraban Kumar Mohanty', 'SKM', 'sraban@iiitdmj.ac.in'],
            ['Pritee Khanna', 'PK', 'pkhanna@iiitdmj.ac.in'],
            ['Ranjeet Kumar Ranjan', 'RKR', 'ranjeet.kr@iiitdmj.ac.in'],
            ['Aparajita Ojha', 'AP', 'aojha@iiitdmj.ac.in'],  # Same professor, different short name
            ['Dada Saheb Ramteke', 'DSR', 'dsramteke@iiitdmj.ac.in'],
            ['Dip Prakash Samajdar', 'SDP', 'dip.samajdar@iiitdmj.ac.in'],  # Same professor, different short name
            ['Sunil Agrawal', 'SA', 'sa@iiitdmj.ac.in'],
            ['Lokendra Kumar Balyan', 'BA', 'balyan@iiitdmj.ac.in'],  # Same professor, different short name
            ['Sanjeev Narayan Sharma', 'SNS', 'snsharma@iiitdmj.ac.in'],
            
            # Add some placeholder professors for the remaining ones
            ['Manoj Kumar', 'MKT', 'mkt@iiitdmj.ac.in'],
            ['S.G. Mahapatra', 'SGM', 'sgm@iiitdmj.ac.in'],
            ['Mohammed Zafar Ali', 'MZA', 'mza@iiitdmj.ac.in'],
            ['Avinash Ravi Raja', 'ARR', 'arr@iiitdmj.ac.in'],
            ['Shivam Mishra', 'ShM', 'shm@iiitdmj.ac.in'],
            ['Deepak Sharma', 'DS', 'ds@iiitdmj.ac.in'],
            ['Tarun Kumar', 'TK', 'tk@iiitdmj.ac.in'],
            ['Chandan Singh', 'ChS', 'chs@iiitdmj.ac.in'],
            ['Anil Sharma', 'AnS', 'ans@iiitdmj.ac.in'],
            ['A.C. Pandey', 'ACP', 'acp@iiitdmj.ac.in'],
            ['V.K. Jain', 'VKJ', 'vkj@iiitdmj.ac.in'],
            ['Mohan Singh', 'MS', 'ms@iiitdmj.ac.in'],
            ['S.K. Singh', 'SKS', 'sks@iiitdmj.ac.in'],
            ['Amit Singh', 'AS', 'as@iiitdmj.ac.in'],
            ['Chandan Das', 'CD', 'cd@iiitdmj.ac.in'],
        ]

        created_count = 0
        updated_count = 0
        skipped_count = 0

        self.stdout.write("Adding professors to database...")
        self.stdout.write("=" * 50)

        for prof_data in professors_data:
            name, short_name, email = prof_data

            # Skip if email is not provided
            if not email or not email.strip():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f"✗ Skipped: {name} - No email provided")
                )
                continue

            try:
                # Split name into first and last name
                name_parts = name.split()
                first_name = name_parts[0]
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else name_parts[0]

                # Create username from email
                username = email.split('@')[0]

                # Check if user already exists by email
                existing_user = User.objects.filter(email=email).first()

                if existing_user:
                    # Check if this is the same professor with different short name
                    if (existing_user.first_name == first_name and 
                        existing_user.last_name == last_name and
                        existing_user.role == 'professor'):
                        
                        # Same professor, different short name - update the short name
                        if existing_user.short_name != short_name:
                            existing_user.short_name = short_name
                            existing_user.save()
                            updated_count += 1
                            self.stdout.write(
                                self.style.WARNING(f"↻ Updated short name: {name} ({short_name}) - {email}")
                            )
                        else:
                            skipped_count += 1
                            self.stdout.write(
                                self.style.WARNING(f"⤳ Already exists: {name} - {email}")
                            )
                    else:
                        # Different professor with same email? This shouldn't happen
                        skipped_count += 1
                        self.stdout.write(
                            self.style.ERROR(f"✗ Email conflict: {email} already used by {existing_user.get_full_name()}")
                        )
                else:
                    # Check if professor exists with same short name but different email
                    existing_by_shortname = User.objects.filter(short_name=short_name, role='professor').first()
                    if existing_by_shortname:
                        skipped_count += 1
                        self.stdout.write(
                            self.style.ERROR(f"✗ Short name conflict: {short_name} already used by {existing_by_shortname.get_full_name()}")
                        )
                    else:
                        # Create new professor user
                        user = User.objects.create_user(
                            username=username,
                            email=email,
                            password='professor123',  # Default password
                            first_name=first_name,
                            last_name=last_name,
                            role='professor',
                            short_name=short_name,
                            email_verified=True
                        )
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"✓ Created: {name} ({short_name}) - {email}")
                        )

            except Exception as e:
                skipped_count += 1
                self.stdout.write(
                    self.style.ERROR(f"✗ Failed: {name} - {email} - Error: {e}")
                )

        self.stdout.write("=" * 50)
        self.stdout.write("PROFESSORS IMPORT SUMMARY:")
        self.stdout.write(f"Created: {created_count}")
        self.stdout.write(f"Updated: {updated_count}")
        self.stdout.write(f"Skipped: {skipped_count}")
        
        # Count total professors
        total_professors = User.objects.filter(role='professor').count()
        self.stdout.write(f"Total professors in database: {total_professors}")
        
        # Show professors with their short names
        self.stdout.write("\nProfessors with short names:")
        for prof in User.objects.filter(role='professor').order_by('short_name'):
            self.stdout.write(f"  {prof.short_name}: {prof.get_full_name()} - {prof.email}")