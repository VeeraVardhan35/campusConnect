from django.core.management.base import BaseCommand
from timetable.models import ClassSchedule, Course, Batch, Classroom, TimeSlot
from users.models import User
from django.db import transaction
from datetime import time

class Command(BaseCommand):
    help = 'Populate ClassSchedule for a specific day using professor short names with automatic missing data creation'

    def add_arguments(self, parser):
        parser.add_argument('day', type=str, help='Day of the week (e.g., monday, tuesday)')

    def handle(self, *args, **options):
        day = options['day'].lower()
        
        # Create missing data first
        self.create_missing_data()
        
        # Get the schedule data for the specific day
        schedule_data = self.get_schedule_data(day)
        
        if not schedule_data:
            self.stdout.write(self.style.ERROR(f"No schedule data defined for {day}"))
            return

        created_count = 0
        error_count = 0

        self.stdout.write(f"Populating ClassSchedule for {day.title()}...")
        self.stdout.write("=" * 50)

        with transaction.atomic():
            for schedule in schedule_data:
                success = self.create_class_schedule(schedule, day)
                if success:
                    created_count += 1
                else:
                    error_count += 1

        self.generate_report(created_count, error_count, day)

    def create_missing_data(self):
        """Create missing courses, professors, classrooms, and batches"""
        self.stdout.write("Checking and creating missing data...")
        
        # Create missing courses
        missing_courses = self.create_missing_courses()
        if missing_courses:
            self.stdout.write(self.style.SUCCESS(f"✓ Created {len(missing_courses)} missing courses"))
        
        # Create missing professors
        missing_professors = self.create_missing_professors()
        if missing_professors:
            self.stdout.write(self.style.SUCCESS(f"✓ Created {len(missing_professors)} missing professors"))
        
        # Create missing classrooms
        missing_classrooms = self.create_missing_classrooms()
        if missing_classrooms:
            self.stdout.write(self.style.SUCCESS(f"✓ Created {len(missing_classrooms)} missing classrooms"))
        
        # Create missing batches
        missing_batches = self.create_missing_batches()
        if missing_batches:
            self.stdout.write(self.style.SUCCESS(f"✓ Created {len(missing_batches)} missing batches"))

    def create_missing_courses(self):
        """Create courses that are referenced in schedule but don't exist"""
        schedule_data = self.get_all_schedule_data()
        course_codes = set()
        
        # Extract all course codes from all days
        for day_data in schedule_data.values():
            for schedule in day_data:
                course_codes.add(schedule[0])  # course_code is first element
        
        missing_courses = []
        existing_courses = set(Course.objects.values_list('code', flat=True))
        
        # Course data for missing courses
        course_data = {
            'EC203': {'name': 'Digital Signal Processing', 'credits': 4, 'discipline': 'ECE'},
            'SM2004': {'name': 'Thermodynamics and Heat Transfer', 'credits': 4, 'discipline': 'SM'},
            'IT2C01': {'name': 'Computer Networks', 'credits': 3, 'discipline': 'CSE'},
            'IT2M01': {'name': 'Machine Learning', 'credits': 3, 'discipline': 'CSE'},
            'IT3E01': {'name': 'VLSI Design', 'credits': 4, 'discipline': 'ECE'},
            'OE3M27': {'name': 'Operations Management', 'credits': 3, 'discipline': 'Common'},
            'OE2M10': {'name': 'Project Management', 'credits': 3, 'discipline': 'Common'},
            'OE3E40': {'name': 'Embedded Systems', 'credits': 3, 'discipline': 'ECE'},
            'OE4E50': {'name': 'Wireless Communication', 'credits': 3, 'discipline': 'ECE'},
            'EC8049': {'name': 'Advanced Communication Systems', 'credits': 3, 'discipline': 'ECE'},
            'OE3N38': {'name': 'Neural Networks', 'credits': 3, 'discipline': 'Common'},
            'CS8016': {'name': 'Cloud Computing', 'credits': 3, 'discipline': 'CSE'},
            'OEM35': {'name': 'Renewable Energy Systems', 'credits': 3, 'discipline': 'Common'},
            'EC5015': {'name': 'Digital Image Processing', 'credits': 3, 'discipline': 'ECE'},
            'EC8030': {'name': 'Optical Communication', 'credits': 3, 'discipline': 'ECE'},
            'CS8004': {'name': 'Software Engineering', 'credits': 3, 'discipline': 'CSE'},
            'EC5M02': {'name': 'Microwave Engineering', 'credits': 3, 'discipline': 'ECE'},
            'CS8037': {'name': 'Data Mining', 'credits': 3, 'discipline': 'CSE'},
            'ME8032': {'name': 'Advanced Manufacturing', 'credits': 3, 'discipline': 'ME'},
            'ME8016': {'name': 'Finite Element Analysis', 'credits': 3, 'discipline': 'ME'},
            'OE4M52': {'name': 'Quality Control', 'credits': 3, 'discipline': 'Common'},
            'EC8004': {'name': 'Satellite Communication', 'credits': 3, 'discipline': 'ECE'},
            'EC5016': {'name': 'Computer Vision', 'credits': 3, 'discipline': 'ECE'},
            'CS8018': {'name': 'Information Security', 'credits': 3, 'discipline': 'CSE'},
            'CS8013': {'name': 'Web Technologies', 'credits': 3, 'discipline': 'CSE'},
            'EC5C01': {'name': 'Communication Networks', 'credits': 3, 'discipline': 'ECE'},
            'DC5N01': {'name': 'Data Compression', 'credits': 3, 'discipline': 'CSE'},
            'CS8007': {'name': 'Mobile Computing', 'credits': 3, 'discipline': 'CSE'},
            'ME8033': {'name': 'Robotics', 'credits': 3, 'discipline': 'ME'},
            'ME8002': {'name': 'CAD/CAM', 'credits': 3, 'discipline': 'ME'},
            'ME8031': {'name': 'Automotive Engineering', 'credits': 3, 'discipline': 'ME'},
            'OE4M76': {'name': 'Industrial Engineering', 'credits': 3, 'discipline': 'Common'},
            'EC5M03': {'name': 'Radar Systems', 'credits': 3, 'discipline': 'ECE'},
            'CS8025': {'name': 'Big Data Analytics', 'credits': 3, 'discipline': 'CSE'},
            'OE4L73': {'name': 'Leadership Skills', 'credits': 3, 'discipline': 'Common'},
            'NP8002': {'name': 'Nanotechnology', 'credits': 3, 'discipline': 'Common'},
            'NS2001': {'name': 'Advanced Mathematics', 'credits': 4, 'discipline': 'Common'},
        }
        
        for code in course_codes:
            if code not in existing_courses:
                course_info = course_data.get(code, {
                    'name': f'{code} - Course',
                    'credits': 3,
                    'discipline': self.get_discipline_from_code(code)
                })
                
                try:
                    Course.objects.create(
                        code=code,
                        name=course_info['name'],
                        credits=course_info['credits']
                    )
                    missing_courses.append(code)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"✗ Failed to create course {code}: {e}"))
        
        return missing_courses

    def create_missing_professors(self):
        """Create professors that are referenced in schedule but don't exist"""
        schedule_data = self.get_all_schedule_data()
        professor_short_names = set()
        
        # Extract all professor short names from all days
        for day_data in schedule_data.values():
            for schedule in day_data:
                prof_short_name = schedule[4]  # professor_short_name is fifth element
                if prof_short_name and prof_short_name.strip():
                    professor_short_names.add(prof_short_name)
        
        missing_professors = []
        existing_professors = set(User.objects.filter(role='professor').values_list('short_name', flat=True))
        
        # Professor data for missing professors
        professor_data = {
            'GF': {'name': 'Gaurav Sharma', 'email': 'gaurav.sharma@iiitdmj.ac.in'},
            'VF': {'name': 'Vikram Singh', 'email': 'vikram.singh@iiitdmj.ac.in'},
            'TC': {'name': 'Tarun Choudhary', 'email': 'tarun.choudhary@iiitdmj.ac.in'},
            'PS': {'name': 'Priya Sharma', 'email': 'priya.sharma@iiitdmj.ac.in'},
            'SKT': {'name': 'S.K. Tiwari', 'email': 'sktiwari@iiitdmj.ac.in'},
            'MDB': {'name': 'M.D. Bansal', 'email': 'mdbansal@iiitdmj.ac.in'},
            'ARR': {'name': 'A.R. Reddy', 'email': 'arreddy@iiitdmj.ac.in'},
            'ShM': {'name': 'Shivam Mishra', 'email': 'shivam.mishra@iiitdmj.ac.in'},
            'DS': {'name': 'Deepak Sharma', 'email': 'deepak.sharma@iiitdmj.ac.in'},
            'BA': {'name': 'B. Arora', 'email': 'b.arora@iiitdmj.ac.in'},
            'TK': {'name': 'Tarun Kumar', 'email': 'tarun.kumar@iiitdmj.ac.in'},
            'ChS': {'name': 'Chandan Singh', 'email': 'chandan.singh@iiitdmj.ac.in'},
            'SNS': {'name': 'S.N. Sharma', 'email': 'sns@iiitdmj.ac.in'},
            'AnS': {'name': 'Anil Sharma', 'email': 'anil.sharma@iiitdmj.ac.in'},
            'ACP': {'name': 'A.C. Pandey', 'email': 'acp@iiitdmj.ac.in'},
            'VKJ': {'name': 'V.K. Jain', 'email': 'vkj@iiitdmj.ac.in'},
            'MS': {'name': 'Mohan Singh', 'email': 'mohan.singh@iiitdmj.ac.in'},
            'SKS': {'name': 'S.K. Singh', 'email': 'sks@iiitdmj.ac.in'},
            'AS': {'name': 'Amit Singh', 'email': 'amit.singh@iiitdmj.ac.in'},
            'CD': {'name': 'Chandan Das', 'email': 'chandan.das@iiitdmj.ac.in'},
            'VMa': {'name': 'V. Mathur', 'email': 'vmathur@iiitdmj.ac.in'},
            'SKC': {'name': 'S.K. Choudhary', 'email': 'skchoudhary@iiitdmj.ac.in'},
            'RP': {'name': 'R. Patel', 'email': 'rpatel@iiitdmj.ac.in'},
        }
        
        for short_name in professor_short_names:
            if short_name not in existing_professors:
                prof_info = professor_data.get(short_name, {
                    'name': f'Professor {short_name}',
                    'email': f'{short_name.lower()}@iiitdmj.ac.in'
                })
                
                try:
                    name_parts = prof_info['name'].split()
                    first_name = name_parts[0]
                    last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else name_parts[0]
                    
                    username = prof_info['email'].split('@')[0]
                    
                    User.objects.create_user(
                        username=username,
                        email=prof_info['email'],
                        password='professor123',
                        first_name=first_name,
                        last_name=last_name,
                        role='professor',
                        short_name=short_name,
                        email_verified=True
                    )
                    missing_professors.append(short_name)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"✗ Failed to create professor {short_name}: {e}"))
        
        return missing_professors

    def create_missing_classrooms(self):
        """Create classrooms that are referenced in schedule but don't exist"""
        schedule_data = self.get_all_schedule_data()
        classroom_numbers = set()
        
        # Extract all classroom numbers from all days
        for day_data in schedule_data.values():
            for schedule in day_data:
                classroom_numbers.add(schedule[5])  # classroom_number is sixth element
        
        missing_classrooms = []
        existing_classrooms = set(Classroom.objects.values_list('room_number', flat=True))
        
        for room_number in classroom_numbers:
            if room_number not in existing_classrooms:
                try:
                    # Determine building and capacity based on room type
                    if room_number.startswith('L'):
                        building = 'LHTC'
                        capacity = 150
                    elif room_number.startswith('CR'):
                        building = 'LHTC'
                        capacity = 80
                    elif 'Lab' in room_number:
                        building = 'CORE LAB COMPLEX'
                        capacity = 30
                    elif room_number == 'ECLab':
                        building = 'CORE LAB COMPLEX'
                        capacity = 30
                    elif room_number == 'PHYLaB':
                        building = 'CORE LAB COMPLEX'
                        capacity = 30
                    else:
                        building = 'LHTC'
                        capacity = 60
                    
                    Classroom.objects.create(
                        room_number=room_number,
                        building=building,
                        capacity=capacity
                    )
                    missing_classrooms.append(room_number)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"✗ Failed to create classroom {room_number}: {e}"))
        
        return missing_classrooms

    def create_missing_batches(self):
        """Create batches that are referenced in schedule but don't exist"""
        schedule_data = self.get_all_schedule_data()
        batch_info_set = set()
        
        # Extract all batch information from all days
        for day_data in schedule_data.values():
            for schedule in day_data:
                batch_year = schedule[1]
                batch_branch = schedule[2]
                batch_section = schedule[3]
                
                # Skip ALL batches as they are handled specially
                if batch_year != 'ALL' and batch_branch != 'ALL' and batch_section:
                    batch_info_set.add((batch_year, batch_branch, batch_section))
        
        missing_batches = []
        
        for batch_year, branch, section in batch_info_set:
            try:
                batch, created = Batch.objects.get_or_create(
                    batch_year=batch_year,
                    branch=branch,
                    section=section,
                    defaults={'name': ''}  # Name will be auto-generated
                )
                if created:
                    missing_batches.append(f"{batch_year}-{branch}-{section}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Failed to create batch {batch_year}-{branch}-{section}: {e}"))
        
        return missing_batches

    def get_discipline_from_code(self, code):
        """Determine discipline from course code"""
        if code.startswith('CS') or code.startswith('IT'):
            return 'CSE'
        elif code.startswith('EC'):
            return 'ECE'
        elif code.startswith('ME'):
            return 'ME'
        elif code.startswith('SM'):
            return 'SM'
        elif code.startswith('DS'):
            return 'DS'
        else:
            return 'Common'

    def get_all_schedule_data(self):
        """Get schedule data for all days"""
        schedules = {}
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        
        for day in days:
            day_data = self.get_schedule_data(day)
            if day_data:
                schedules[day] = day_data
        
        return schedules

    def get_schedule_data(self, day):
        """Return schedule data for the specific day using professor short names"""
        schedules = {
            'monday': [
                # Your existing Monday schedule data from add_all.py
                ('NS1001', '2025', 'cs', 'A', 'DM', 'L106', '10:00', '11:00'),
                ('ES1002', '2025', 'cs', 'A', 'PKP', 'L106', '11:00', '12:00'),
                ('IT1001', '2025', 'cs', 'A', 'RKS', 'L106', '12:00', '13:00'),
                ('ES1002', '2025', 'cs', 'A', 'PKP', 'ECLab1', '14:00', '16:00'),
                ('NS1002', '2025', 'cs', 'A', 'ACM', 'PhyLab1', '16:00', '18:00'),
                # ... include all your existing schedule data for Monday
            ],
            'wednesday': [
                # Your existing Wednesday schedule data
                ('HS1001', '2025', 'sm', 'A', 'MA', 'L102', '09:00', '10:00'),
                ('HS1001', '2025', 'sm', 'B', 'MA', 'L102', '09:00', '10:00'),
                # ... include all your existing schedule data for Wednesday
            ],
            # Add other days as needed
        }
        return schedules.get(day, [])

    def create_class_schedule(self, schedule_data, day):
        """Create a single class schedule using professor short name"""
        try:
            (course_code, batch_year, batch_branch, batch_section, 
             professor_short_name, classroom_number, start_time_str, end_time_str) = schedule_data

            # Skip if no professor short name provided
            if not professor_short_name or not professor_short_name.strip():
                self.stdout.write(self.style.WARNING(f"↻ Skipped: No professor for {course_code}"))
                return False

            # Convert time strings to time objects
            start_time = time(*map(int, start_time_str.split(':')))
            end_time = time(*map(int, end_time_str.split(':')))

            # Get or create objects with fallbacks
            try:
                course = Course.objects.get(code=course_code)
            except Course.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"✗ Course not found (even after creation attempt): {course_code}"))
                return False

            try:
                professor = User.objects.get(short_name=professor_short_name, role='professor')
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"✗ Professor not found (even after creation attempt): {professor_short_name}"))
                return False

            try:
                classroom = Classroom.objects.get(room_number=classroom_number)
            except Classroom.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"✗ Classroom not found (even after creation attempt): {classroom_number}"))
                return False

            # Handle ALL batches specially
            if batch_year == 'ALL' or batch_branch == 'ALL':
                return self.handle_all_batches(course, professor, classroom, day, start_time, end_time, 
                                             batch_year, batch_branch, batch_section, start_time_str, end_time_str)
            
            try:
                batch = Batch.objects.get(
                    batch_year=batch_year,
                    branch=batch_branch, 
                    section=batch_section
                )
            except Batch.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"✗ Batch not found (even after creation attempt): {batch_year} {batch_branch} {batch_section}"))
                return False
            
            # Get or create time slot
            time_slot, created_ts = TimeSlot.objects.get_or_create(
                day=day,
                start_time=start_time,
                end_time=end_time,
                defaults={
                    'day': day,
                    'start_time': start_time,
                    'end_time': end_time
                }
            )

            # Check for conflicts
            classroom_conflict = ClassSchedule.objects.filter(
                classroom=classroom,
                time_slot=time_slot
            ).exists()

            if classroom_conflict:
                self.stdout.write(
                    self.style.WARNING(f"↻ Classroom conflict: {classroom.room_number} at {start_time_str}-{end_time_str}")
                )
                return False

            batch_conflict = ClassSchedule.objects.filter(
                batch=batch,
                time_slot=time_slot
            ).exists()

            if batch_conflict:
                self.stdout.write(
                    self.style.WARNING(f"↻ Batch conflict: {batch} at {start_time_str}-{end_time_str}")
                )
                return False

            # Create class schedule
            class_schedule, created = ClassSchedule.objects.get_or_create(
                course=course,
                professor=professor,
                batch=batch,
                classroom=classroom,
                time_slot=time_slot
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ {start_time_str}-{end_time_str}: {course.code} for {batch} "
                        f"with Prof. {professor.short_name} in {classroom.room_number}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"↻ Already exists: {course.code} for {batch} at {start_time_str}")
                )

            return True

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Error creating schedule: {e}"))
            return False

    def handle_all_batches(self, course, professor, classroom, day, start_time, end_time,
                         batch_year, batch_branch, batch_section, start_time_str, end_time_str):
        """Handle ALL batches by distributing across different classrooms"""
        created_count = 0

        # Get all batches based on the ALL parameters
        batches = self.get_batches_for_schedule(batch_year, batch_branch, batch_section)
        
        if not batches:
            self.stdout.write(self.style.WARNING(f"↻ No batches found for: {batch_year}/{batch_branch}/{batch_section}"))
            return False

        # Get or create time slot
        time_slot, created_ts = TimeSlot.objects.get_or_create(
            day=day,
            start_time=start_time,
            end_time=end_time,
            defaults={
                'day': day,
                'start_time': start_time,
                'end_time': end_time
            }
        )

        # Group batches and assign to different classrooms to avoid conflicts
        classroom_options = self.get_alternative_classrooms(classroom.room_number)
        
        self.stdout.write(f"Processing ALL batches for {course.code} - Distributing across classrooms...")

        for i, batch in enumerate(batches):
            # Use different classroom for each batch to avoid conflicts
            current_classroom_num = classroom_options[i % len(classroom_options)]
            try:
                current_classroom = Classroom.objects.get(room_number=current_classroom_num)
                
                # Check for conflicts
                classroom_conflict = ClassSchedule.objects.filter(
                    classroom=current_classroom,
                    time_slot=time_slot
                ).exists()

                batch_conflict = ClassSchedule.objects.filter(
                    batch=batch,
                    time_slot=time_slot
                ).exists()

                if classroom_conflict or batch_conflict:
                    self.stdout.write(
                        self.style.WARNING(f"↻ Conflict for {batch} in {current_classroom.room_number}")
                    )
                    continue

                # Create class schedule
                class_schedule, created = ClassSchedule.objects.get_or_create(
                    course=course,
                    professor=professor,
                    batch=batch,
                    classroom=current_classroom,
                    time_slot=time_slot
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ {start_time_str}-{end_time_str}: {course.code} for {batch} "
                            f"with Prof. {professor.short_name} in {current_classroom.room_number}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"↻ Already exists: {course.code} for {batch} at {start_time_str}")
                    )

            except Classroom.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"✗ Alternative classroom not found: {current_classroom_num}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Error creating schedule for {batch}: {e}"))

        return created_count > 0

    def get_batches_for_schedule(self, batch_year, batch_branch, batch_section):
        """Get batches based on ALL parameters - returns actual Batch objects"""
        batches = Batch.objects.all()
        
        # Handle batch_year - get actual batch years from database
        if batch_year != 'ALL':
            batches = batches.filter(batch_year=batch_year)
        else:
            # Get all distinct batch years that exist
            available_years = Batch.objects.values_list('batch_year', flat=True).distinct()
            if available_years:
                batches = batches.filter(batch_year__in=available_years)
        
        # Handle batch_branch - get actual branches from database
        if batch_branch != 'ALL':
            batches = batches.filter(branch=batch_branch)
        else:
            # Get all distinct branches that exist
            available_branches = Batch.objects.values_list('branch', flat=True).distinct()
            if available_branches:
                batches = batches.filter(branch__in=available_branches)
        
        # Handle batch_section
        if batch_section and batch_section.strip():  # If section is provided and not empty
            batches = batches.filter(section=batch_section)
        
        return batches

    def get_alternative_classrooms(self, original_classroom):
        """Get alternative classrooms when the original is occupied"""
        # Define classroom groups that can be used as alternatives
        classroom_groups = {
            'L101': ['L101', 'L102', 'L103', 'L104', 'L105', 'L106'],
            'L102': ['L102', 'L101', 'L103', 'L104', 'L105', 'L106'],
            'L201': ['L201', 'L202', 'L203', 'L204', 'L205', 'L206'],
            'L202': ['L202', 'L201', 'L203', 'L204', 'L205', 'L206'],
            'CR101': ['CR101', 'CR102', 'CR103', 'CR104', 'CR105'],
            'CR102': ['CR102', 'CR101', 'CR103', 'CR104', 'CR105'],
            'CR107': ['CR107', 'CR108', 'CR109', 'CR201', 'CR202'],
            'CR202': ['CR202', 'CR201', 'CR203', 'CR204', 'CR205'],
            'L104': ['L104', 'L105', 'L106', 'L107', 'L201', 'L202'],
            'L207': ['L207', 'L206', 'L205', 'L107', 'L106'],
        }
        
        return classroom_groups.get(original_classroom, [original_classroom])

    def generate_report(self, created_count, error_count, day):
        """Generate report for the day"""
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(f"{day.upper()} SCHEDULE POPULATION SUMMARY:")
        self.stdout.write("=" * 50)
        
        self.stdout.write(f"Classes Created: {created_count}")
        self.stdout.write(f"Errors: {error_count}")
        
        # Show today's schedule
        today_classes = ClassSchedule.objects.filter(time_slot__day=day).select_related(
            'course', 'professor', 'batch', 'classroom', 'time_slot'
        ).order_by('time_slot__start_time')
        
        self.stdout.write(f"\n{day.title()}'s Schedule ({today_classes.count()} classes):")
        self.stdout.write("-" * 50)
        
        for cls in today_classes:
            self.stdout.write(
                f"  {cls.time_slot.start_time.strftime('%H:%M')}-{cls.time_slot.end_time.strftime('%H:%M')}: "
                f"{cls.course.code} - {cls.batch} - {cls.classroom.room_number} - "
                f"Prof. {cls.professor.short_name}"
            )

        if error_count == 0:
            self.stdout.write(
                self.style.SUCCESS(f"\n✅ {day.title()} schedule population completed successfully!")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"\n⚠️  {day.title()} schedule completed with {error_count} errors.")
            )