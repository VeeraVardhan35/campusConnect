from django.core.management.base import BaseCommand
from timetable.models import ClassSchedule, Course, Batch, Classroom, TimeSlot
from users.models import User
from django.db import transaction
from datetime import time

class Command(BaseCommand):
    help = 'AGGRESSIVE FIX: Force create all Wednesday classes'

    def handle(self, *args, **options):
        self.stdout.write("🚀 AGGRESSIVE WEDNESDAY SCHEDULE FIX")
        self.stdout.write("=" * 60)
        
        # Step 1: Clear existing Wednesday data
        self.clear_wednesday_data()
        
        # Step 2: Create all missing data
        self.create_all_missing_data()
        
        # Step 3: Create Wednesday schedule with forced distribution
        self.create_wednesday_schedule_aggressive()
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("🎯 WEDNESDAY SCHEDULE FIX COMPLETED!")
        self.stdout.write("=" * 60)

    def clear_wednesday_data(self):
        """Clear all existing Wednesday schedules"""
        self.stdout.write("\n1. CLEARING EXISTING WEDNESDAY DATA...")
        
        wednesday_classes = ClassSchedule.objects.filter(time_slot__day='wednesday')
        wednesday_slots = TimeSlot.objects.filter(day='wednesday')
        
        self.stdout.write(f"   Deleting {wednesday_classes.count()} Wednesday classes")
        self.stdout.write(f"   Deleting {wednesday_slots.count()} Wednesday time slots")
        
        wednesday_classes.delete()
        wednesday_slots.delete()
        
        self.stdout.write("   ✅ Wednesday data cleared successfully!")

    def create_all_missing_data(self):
        """Create all missing courses, professors, classrooms, and batches"""
        self.stdout.write("\n2. CREATING ALL MISSING DATA...")
        
        # Create any missing classrooms first
        self.create_all_classrooms()
        
        # Create missing professors for empty short names
        self.create_missing_professors()

    def create_all_classrooms(self):
        """Ensure all classrooms exist"""
        self.stdout.write("   🏫 Ensuring all classrooms exist...")
        
        all_classrooms = [
            # Lecture Halls
            'L101', 'L102', 'L103', 'L104', 'L105', 'L106', 'L107',
            'L201', 'L202', 'L203', 'L204', 'L205', 'L206', 'L207',
            # Computer Labs
            'CR101', 'CR102', 'CR103', 'CR104', 'CR105', 'CR106', 'CR107', 'CR108', 'CR109',
            'CR201', 'CR202', 'CR203', 'CR204', 'CR205', 'CR206',
            # Library
            'CC-GF', 'CC-FF', 'CC-SF',
            # Labs
            'ECLab1', 'ECLab2', 'ECLab3', 'VLSILab', 'PhyLab1', 'PhyLab2', 'PhyLab3',
            'ChemLab1', 'ChemLab2', 'MechLab1', 'MechLab2', 'MechLab3', 'CADLab', 
            'FMHTLab', 'AMPLab', 'MFLab', 'CPPSLab',
            # Others
            'Workshop1', 'Workshop2', 'DesignStudio1', 'DesignStudio2', 'DesignStudio3',
            'Auditorium', 'ECLab', 'PHYLaB'
        ]
        
        for room_number in all_classrooms:
            try:
                if room_number.startswith('L'):
                    building = 'LHTC'
                    capacity = 150
                elif room_number.startswith('CR'):
                    building = 'LHTC'
                    capacity = 80
                elif room_number.startswith('CC-'):
                    building = 'LIBRARY'
                    capacity = 80
                elif 'Lab' in room_number or room_number in ['ECLab', 'PHYLaB']:
                    building = 'CORE LAB COMPLEX'
                    capacity = 30
                else:
                    building = 'LHTC'
                    capacity = 60
                
                Classroom.objects.get_or_create(
                    room_number=room_number,
                    defaults={
                        'building': building,
                        'capacity': capacity
                    }
                )
            except Exception as e:
                self.stdout.write(f"      ❌ Failed to create classroom {room_number}: {e}")

    def create_missing_professors(self):
        """Create professors for empty short names"""
        self.stdout.write("   👨‍🏫 Creating professors for empty slots...")
        
        # Professors needed for empty slots
        missing_profs = {
            'AM': 'Auto Professor AM',
            'GF': 'Auto Professor GF', 
            'VF': 'Auto Professor VF',
            'TC': 'Auto Professor TC',
            'PS': 'Auto Professor PS',
            'SKT': 'Auto Professor SKT',
            'MDB': 'Auto Professor MDB',
            'ARR': 'Auto Professor ARR',
            'ShM': 'Auto Professor ShM',
            'DS': 'Auto Professor DS',
            'BA': 'Auto Professor BA',
            'TK': 'Auto Professor TK',
            'ChS': 'Auto Professor ChS',
            'SNS': 'Auto Professor SNS',
            'AnS': 'Auto Professor AnS',
            'ACP': 'Auto Professor ACP',
            'VKJ': 'Auto Professor VKJ',
            'MS': 'Auto Professor MS',
            'SKS': 'Auto Professor SKS',
            'AS': 'Auto Professor AS',
            'CD': 'Auto Professor CD',
            'VMa': 'Auto Professor VMa',
            'SKC': 'Auto Professor SKC',
            'RP': 'Auto Professor RP',
            'SA': 'Auto Professor SA'
        }
        
        for short_name, full_name in missing_profs.items():
            try:
                User.objects.get_or_create(
                    short_name=short_name,
                    role='professor',
                    defaults={
                        'username': f'prof_{short_name.lower()}',
                        'email': f'{short_name.lower()}@iiitdmj.ac.in',
                        'password': 'professor123',
                        'first_name': full_name,
                        'last_name': '',
                        'email_verified': True
                    }
                )
            except Exception as e:
                self.stdout.write(f"      ❌ Failed to create professor {short_name}: {e}")

    def create_wednesday_schedule_aggressive(self):
        """Force create all Wednesday classes with intelligent distribution"""
        self.stdout.write("\n3. AGGRESSIVELY CREATING WEDNESDAY SCHEDULE...")
        
        wednesday_schedule = self.get_wednesday_schedule()
        total_classes = len(wednesday_schedule)
        success_count = 0
        
        self.stdout.write(f"   Processing {total_classes} classes...")
        
        # Group by time slot and distribute classrooms
        time_slots = {}
        for schedule in wednesday_schedule:
            time_key = f"{schedule[6]}-{schedule[7]}"
            if time_key not in time_slots:
                time_slots[time_key] = []
            time_slots[time_key].append(schedule)
        
        # Process each time slot
        for time_key, schedules in time_slots.items():
            self.stdout.write(f"\n   ⏰ Time Slot {time_key}: {len(schedules)} classes")
            
            # Get all available classrooms for this time
            available_classrooms = list(Classroom.objects.all())
            
            for i, schedule in enumerate(schedules):
                classroom = available_classrooms[i % len(available_classrooms)]
                success = self.force_create_class(schedule, time_key, classroom)
                if success:
                    success_count += 1
        
        self.stdout.write(f"\n   📊 FINAL RESULTS: {success_count}/{total_classes} classes created!")
        
        # Show summary
        self.show_wednesday_summary()

    def force_create_class(self, schedule_data, time_key, classroom):
        """Force create a class with the assigned classroom"""
        try:
            (course_code, batch_year, batch_branch, batch_section, 
             professor_short_name, original_classroom, start_time_str, end_time_str) = schedule_data

            # Handle empty professor - use a default
            if not professor_short_name or not professor_short_name.strip():
                professor_short_name = 'AM'  # Default professor

            # Convert time
            start_time = time(*map(int, start_time_str.split(':')))
            end_time = time(*map(int, end_time_str.split(':')))

            # Get objects
            course = Course.objects.get(code=course_code)
            professor = User.objects.get(short_name=professor_short_name, role='professor')
            
            # Handle batch
            if batch_year == 'ALL' or batch_branch == 'ALL':
                # For ALL batches, pick the first batch of that type
                if batch_branch == 'ALL':
                    batch = Batch.objects.first()
                else:
                    batch = Batch.objects.filter(branch=batch_branch).first()
                if not batch:
                    self.stdout.write(f"      ⚠️  No batch found for {course_code}")
                    return False
            else:
                batch = Batch.objects.get(
                    batch_year=batch_year,
                    branch=batch_branch,
                    section=batch_section
                )

            # Get or create time slot
            time_slot, created = TimeSlot.objects.get_or_create(
                day='wednesday',
                start_time=start_time,
                end_time=end_time,
                defaults={
                    'day': 'wednesday',
                    'start_time': start_time,
                    'end_time': end_time
                }
            )

            # Force create (update if exists)
            class_schedule, created = ClassSchedule.objects.update_or_create(
                course=course,
                batch=batch,
                time_slot=time_slot,
                defaults={
                    'professor': professor,
                    'classroom': classroom
                }
            )

            status = "✅ CREATED" if created else "🔄 UPDATED"
            self.stdout.write(
                f"      {status} {start_time_str}-{end_time_str}: {course_code} for {batch} "
                f"with Prof. {professor.short_name} in {classroom.room_number}"
            )

            return True

        except Exception as e:
            self.stdout.write(f"      ❌ Failed {course_code}: {str(e)}")
            return False

    def show_wednesday_summary(self):
        """Show final Wednesday schedule"""
        self.stdout.write("\n4. WEDNESDAY SCHEDULE SUMMARY:")
        self.stdout.write("=" * 60)
        
        from collections import defaultdict
        schedule_by_time = defaultdict(list)
        
        wednesday_classes = ClassSchedule.objects.filter(
            time_slot__day='wednesday'
        ).select_related('course', 'batch', 'classroom', 'time_slot', 'professor')
        
        for cls in wednesday_classes:
            time_key = f"{cls.time_slot.start_time.strftime('%H:%M')}-{cls.time_slot.end_time.strftime('%H:%M')}"
            schedule_by_time[time_key].append(cls)
        
        for time_key in sorted(schedule_by_time.keys()):
            self.stdout.write(f"\n🕒 {time_key}:")
            for cls in schedule_by_time[time_key]:
                self.stdout.write(
                    f"   📚 {cls.course.code} - {cls.batch} - "
                    f"🏫 {cls.classroom.room_number} - 👨‍🏫 Prof. {cls.professor.short_name}"
                )
        
        self.stdout.write(f"\n📈 TOTAL WEDNESDAY CLASSES: {wednesday_classes.count()}")

    def get_wednesday_schedule(self):
        """Return complete Wednesday schedule data"""
        return [
            # Fixed Wednesday schedule with distributed classrooms
            ('HS1001', '2025', 'sm', 'A', 'MA', 'L101', '09:00', '10:00'),
            ('HS1001', '2025', 'sm', 'B', 'MA', 'L102', '09:00', '10:00'),
            ('HS1001', '2025', 'me', 'A', 'MA', 'L103', '09:00', '10:00'),
            ('HS1001', '2025', 'me', 'B', 'MA', 'L104', '09:00', '10:00'),

            ('NS1001', '2025', 'cs', 'A', 'DM', 'L105', '10:00', '11:00'),
            ('NS1001', '2025', 'cs', 'B', 'NKM', 'L106', '10:00', '11:00'),
            ('NS1001', '2025', 'ec', 'A', 'SSL', 'L201', '10:00', '11:00'),
            ('NS1001', '2025', 'ec', 'B', 'SSL', 'L202', '10:00', '11:00'),

            ('ES1002', '2025', 'cs', 'A', 'PKP', 'L203', '11:00', '12:00'),
            ('ES1002', '2025', 'cs', 'B', 'PR',  'L204', '11:00', '12:00'),
            ('HS1001', '2025', 'ec', 'A', 'MA', 'L205', '11:00', '12:00'),
            ('HS1001', '2025', 'ec', 'B', 'MA', 'L206', '11:00', '12:00'),

            ('IT1002', '2025', 'ec', 'A', 'AV', 'L101', '12:00', '13:00'),
            ('IT1002', '2025', 'ec', 'B', 'AV', 'L102', '12:00', '13:00'),
            ('DS1005', '2025', 'sm', 'A', 'AM', 'L103', '12:00', '13:00'),
            ('DS1005', '2025', 'sm', 'B', 'AM', 'L104', '12:00', '13:00'),

            ('HS1001', '2025', 'cs', 'A', 'JAMF', 'L105', '14:00', '15:00'),
            ('DS1005', '2025', 'ec', 'A', 'JKT', 'L201', '14:00', '15:00'),
            ('DS1005', '2025', 'ec', 'B', 'JKT', 'L202', '14:00', '15:00'),

            ('ES1002', '2025', 'cs', 'B', 'PR',  'ECLab1', '14:00', '16:00'),
            ('ES1002', '2025', 'cs', 'A', 'PKP', 'ECLab2', '16:00', '18:00'),

            ('IT1002', '2025', 'me', 'A', 'MKT', 'CC-GF', '15:00', '18:00'),
            ('IT1002', '2025', 'me', 'B', 'MKT', 'CC-FF', '15:00', '18:00'),

            ('DS1005', '2024', 'sm', 'A', 'MKT', 'CR101', '15:00', '18:00'),
            ('DS1005', '2024', 'sm', 'B', 'MKT', 'CR102', '15:00', '18:00'),
            ('CS2002', '2024', 'cs', 'B', 'RKR', 'L106', '09:00', '10:00'),
            ('IT2002', '2024', 'ec', 'A', 'GF', 'L107', '09:00', '10:00'),
            ('IT2002', '2024', 'ec', 'B', 'GF', 'CR103', '09:00', '10:00'),
            ('IT2002', '2024', 'sm', 'A', 'RKS', 'CR104', '09:00', '10:00'),
            ('IT2002', '2024', 'sm', 'B', 'RKS', 'CR105', '09:00', '10:00'),
            ('IT2002', '2024', 'me', 'A', 'RKS', 'CR106', '09:00', '10:00'),
            ('IT2002', '2024', 'me', 'B', 'RKS', 'CR107', '09:00', '10:00'),

            ('IT2C01', '2024', 'cs', 'A', 'AS', 'CC-SF', '09:00', '12:00'),

            ('CS2002', '2024', 'cs', 'B', 'RKR', 'L101', '10:00', '11:00'),
            ('EC204',  '2024', 'ec', 'A', 'PNK', 'L102', '10:00', '11:00'),
            ('EC204',  '2024', 'ec', 'B', 'PNK', 'L103', '10:00', '11:00'),
            ('SM2004', '2024', 'sm', 'A', 'TC', 'CR108', '10:00', '11:00'),
            ('SM2004', '2024', 'sm', 'B', 'TC', 'CR109', '10:00', '11:00'),

            ('CS2003', '2024', 'cs', 'B', 'PK', 'L104', '11:00', '12:00'),
            ('IT2M01', '2024', 'me', 'A', 'DSR', 'CR201', '10:00', '13:00'),
            ('IT2M01', '2024', 'me', 'B', 'DSR', 'CR202', '10:00', '13:00'),
            ('IT2002', '2024', 'ec', 'A', 'VF', 'CR203', '11:00', '12:00'),
            ('IT2002', '2024', 'ec', 'B', 'VF', 'CR204', '11:00', '12:00'),

            ('CS2003', '2024', 'cs', 'A', 'PK', 'L105', '12:00', '13:00'),
            ('IT2001', '2024', 'cs', 'B', 'SKM', 'L106', '12:00', '13:00'),

            ('CS2002', '2024', 'cs', 'A', 'RKR', 'L201', '14:00', '15:00'),
            ('EC2002', '2024', 'ec', 'A', 'PS', 'L202', '14:00', '15:00'),
            ('EC2002', '2024', 'ec', 'B', 'PS', 'L203', '14:00', '15:00'),
            ('ME2002', '2024', 'me', 'A', 'MS', 'CR205', '14:00', '15:00'),
            ('ME2002', '2024', 'me', 'B', 'MS', 'CR206', '14:00', '15:00'),

            ('IT2001', '2024', 'cs', 'A', 'SKM', 'L204', '15:00', '16:00'),
            ('EC203',  '2024', 'ec', 'A', 'SKT', 'L205', '15:00', '16:00'),
            ('EC203',  '2024', 'ec', 'B', 'SKT', 'L206', '15:00', '16:00'),
            ('SM2002', '2024', 'sm', 'A', 'SGM', 'PhyLab1', '14:00', '16:00'),

            ('IT2001', '2024', 'ec', 'A', 'VF', 'VLSILab', '16:00', '18:00'),
            ('IT2001', '2024', 'ec', 'B', 'VF', 'PhyLab2', '16:00', '18:00'),

            ('ME2003', '2024', 'me', 'A', 'VKG', 'MechLab1', '16:00', '17:00'),
            ('ME2003', '2024', 'me', 'B', 'VKG', 'MechLab2', '16:00', '17:00'),

            ('NS2001', '2024', 'cs', 'A', 'VF', 'L101', '17:00', '18:00'),

            ('IT2002', '2024', 'sm', 'A', 'RKS', 'L102', '17:00', '18:00'),
            ('IT2002', '2024', 'sm', 'B', 'RKS', 'L103', '17:00', '18:00'),
            ('IT2002', '2024', 'me', 'A', 'RKS', 'L104', '17:00', '18:00'),
            ('IT2002', '2024', 'me', 'B', 'RKS', 'L105', '17:00', '18:00'),
            ('IT3E01', '2023', 'ec', 'A', 'KD', 'ECLab3', '09:00', '12:00'),
            ('IT3E01', '2023', 'ec', 'B', 'KD', 'CADLab', '09:00', '12:00'),

            ('ME3011', '2023', 'me', 'A', 'SKC', 'FMHTLab', '10:00', '11:00'),
            ('ME3011', '2023', 'me', 'B', 'SKC', 'AMPLab', '10:00', '11:00'),
            ('SM3011', '2023', 'sm', 'A', 'TS',  'MFLab', '10:00', '11:00'),
            ('SM3011', '2023', 'sm', 'B', 'TS',  'CPPSLab', '10:00', '11:00'),

            ('SM3009', '2023', 'sm', 'A', 'KP', 'Workshop1', '11:00', '12:00'),
            ('SM3009', '2023', 'sm', 'B', 'KP', 'Workshop2', '11:00', '12:00'),

            ('OE3M27', '2023', 'ALL', 'ALL', 'SM',  'DesignStudio1', '12:00', '13:00'),
            ('OE2M10', '2023', 'ALL', 'ALL', 'TC',  'DesignStudio2', '12:00', '13:00'),
            ('OE3E40', '2023', 'ALL', 'ALL', 'SNS', 'DesignStudio3', '12:00', '13:00'),
            ('OE4E50', '2023', 'ALL', 'ALL', 'SKT', 'Auditorium', '12:00', '13:00'),
            ('EC8049', '2023', 'ALL', 'ALL', 'KD',  'ChemLab1', '12:00', '13:00'),
            ('OE3N38', '2023', 'ALL', 'ALL', 'NRJ', 'ChemLab2', '12:00', '13:00'),
            ('CS8016', '2023', 'ALL', 'ALL', 'VMa', 'L107', '12:00', '13:00'),

            ('CS3009', '2023', 'cs', 'A', 'ShM', 'L201', '14:00', '15:00'),
            ('CS3010', '2023', 'cs', 'B', 'AG',  'L202', '14:00', '15:00'),
            ('SM3010', '2023', 'sm', 'A', 'ARR', 'L203', '14:00', '15:00'),
            ('SM3010', '2023', 'sm', 'B', 'ARR', 'L204', '14:00', '15:00'),

            ('CS3010', '2023', 'cs', 'A', 'AG',  'L205', '15:00', '16:00'),
            ('CS3009', '2023', 'cs', 'B', 'ShM', 'L206', '15:00', '16:00'),

            ('IT3E01', '2023', 'ec', 'A', 'KD', 'ECLab1', '14:00', '17:00'),
            ('IT3E01', '2023', 'ec', 'B', 'KD', 'ECLab2', '14:00', '17:00'),

            ('SM3012', '2023', 'sm', 'B', 'SA', 'PhyLab3', '15:00', '17:00'),

            ('CS3011', '2023', 'cs', 'A', 'DS', 'L101', '16:00', '17:00'),
        ]