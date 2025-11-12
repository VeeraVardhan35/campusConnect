from django.core.management.base import BaseCommand
from timetable.models import Classroom

class Command(BaseCommand):
    help = 'Add classrooms to the database'

    def handle(self, *args, **options):
        classrooms_data = [
            # Lecture Halls
            {'room_number': 'L101', 'building': 'LHTC', 'capacity': 150},
            {'room_number': 'L102', 'building': 'LHTC', 'capacity': 150},
            {'room_number': 'L103', 'building': 'LHTC', 'capacity': 150},
            {'room_number': 'L104', 'building': 'LHTC', 'capacity': 150},
            {'room_number': 'L105', 'building': 'LHTC', 'capacity': 150},
            {'room_number': 'L106', 'building': 'LHTC', 'capacity': 150},
            {'room_number': 'L107', 'building': 'LHTC', 'capacity': 150},
            
            {'room_number': 'L201', 'building': 'LHTC', 'capacity': 150},
            {'room_number': 'L202', 'building': 'LHTC', 'capacity': 150},
            {'room_number': 'L203', 'building': 'LHTC', 'capacity': 150},
            {'room_number': 'L204', 'building': 'LHTC', 'capacity': 150},
            {'room_number': 'L205', 'building': 'LHTC', 'capacity': 150},
            {'room_number': 'L206', 'building': 'LHTC', 'capacity': 150},
   
            # {'room_number': 'L302', 'building': 'Main Building', 'capacity': 60},
            # {'room_number': 'L303', 'building': 'Main Building', 'capacity': 60},
            # {'room_number': 'L304', 'building': 'Main Building', 'capacity': 60},
            # {'room_number': 'L305', 'building': 'Main Building', 'capacity': 60},
            # {'room_number': 'L306', 'building': 'Main Building', 'capacity': 60},
            # {'room_number': 'L307', 'building': 'Main Building', 'capacity': 60},
            # {'room_number': 'L308', 'building': 'Main Building', 'capacity': 60},
            
            # # Seminar Halls
            # {'room_number': 'SH1', 'building': 'LHTC', 'capacity': 120},
            # {'room_number': 'SH2', 'building': 'LHTC', 'capacity': 120},
            # {'room_number': 'SH3', 'building': '', 'capacity': 120},
            
            # Computer Labs
            {'room_number': 'CR101', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR102', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR103', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR104', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR105', 'building': 'LHTC', 'capacity': 80},
            
            {'room_number': 'CR106', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR107', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR108', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR109', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR201', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR202', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR203', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR204', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR205', 'building': 'LHTC', 'capacity': 80},
            {'room_number': 'CR206', 'building': 'LHTC', 'capacity': 80},

            # Library
            {'room_number': 'CC-GF', 'building': 'LIBRARY', 'capacity': 80},
            {'room_number': 'CC-FF', 'building': 'LIBRARY', 'capacity': 80},
            {'room_number': 'CC-SF', 'building': 'LIBRARY', 'capacity': 80},
            # Electronics Labs
            {'room_number': 'ECLab1', 'building': 'CORE LAB COMPLEX', 'capacity': 30},
            {'room_number': 'ECLab2', 'building': 'CORE LAB COMPLEX', 'capacity': 30},
            {'room_number': 'ECLab3', 'building': 'CORE LAB COMPLEX', 'capacity': 30},
            {'room_number': 'VLSILab', 'building': 'CORE LAB COMPLEX', 'capacity': 25},
            
            # Physics Labs
            {'room_number': 'PhyLab1', 'building': 'CORE LAB COMPLEX', 'capacity': 30},
            {'room_number': 'PhyLab2', 'building': 'CORE LAB COMPLEX', 'capacity': 30},
            {'room_number': 'PhyLab3', 'building': 'CORE LAB COMPLEX', 'capacity': 30},
            
            # Chemistry Labs
            {'room_number': 'ChemLab1', 'building': 'Science Building', 'capacity': 30},
            {'room_number': 'ChemLab2', 'building': 'Science Building', 'capacity': 30},
            
            # Mechanical Labs
            {'room_number': 'MechLab1', 'building': 'ME Building', 'capacity': 25},
            {'room_number': 'MechLab2', 'building': 'ME Building', 'capacity': 25},
            {'room_number': 'MechLab3', 'building': 'ME Building', 'capacity': 25},
            {'room_number': 'CADLab', 'building': 'ME Building', 'capacity': 40},
            {'room_number': 'FMHTLab', 'building': 'ME Building', 'capacity': 40},
            {'room_number': 'AMPLab', 'building': 'ME Building', 'capacity': 40},
            {'room_number': 'MFLab', 'building': 'ME Building', 'capacity': 40},
            {'room_number': 'CPPSLab', 'building': 'ME Building', 'capacity': 40},
            
            # Workshop
            {'room_number': 'Workshop1', 'building': 'Workshop Building', 'capacity': 20},
            {'room_number': 'Workshop2', 'building': 'Workshop Building', 'capacity': 20},
            
            # Design Studio
            {'room_number': 'DesignStudio1', 'building': 'LHTC', 'capacity': 25},
            {'room_number': 'DesignStudio2', 'building': 'LHTC', 'capacity': 25},
            {'room_number': 'DesignStudio3', 'building': 'LHTC', 'capacity': 25},
            
            # # Conference Rooms
            # {'room_number': 'CR1', 'building': 'Admin Building', 'capacity': 50},
            # {'room_number': 'CR2', 'building': 'Admin Building', 'capacity': 30},
            # {'room_number': 'CR3', 'building': 'Admin Building', 'capacity': 20},
            
            # Auditorium
            {'room_number': 'Auditorium', 'building': 'LHTC', 'capacity': 300},
        ]

        created_count = 0
        updated_count = 0
        skipped_count = 0

        self.stdout.write("Adding classrooms to database...")
        self.stdout.write("=" * 50)

        for classroom_data in classrooms_data:
            room_number = classroom_data['room_number']
            building = classroom_data['building']
            capacity = classroom_data['capacity']

            try:
                # Try to get existing classroom or create new one
                classroom, created = Classroom.objects.get_or_create(
                    room_number=room_number,
                    defaults={
                        'building': building,
                        'capacity': capacity
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ Created: {building} - {room_number} (Capacity: {capacity})")
                    )
                else:
                    # Update existing classroom if needed
                    if classroom.building != building or classroom.capacity != capacity:
                        classroom.building = building
                        classroom.capacity = capacity
                        classroom.save()
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f"↻ Updated: {building} - {room_number} (Capacity: {capacity})")
                        )
                    else:
                        skipped_count += 1
                        self.stdout.write(
                            self.style.WARNING(f"⤳ Already exists: {building} - {room_number}")
                        )

            except Exception as e:
                skipped_count += 1
                self.stdout.write(
                    self.style.ERROR(f"✗ Failed: {building} - {room_number} - Error: {e}")
                )

        self.stdout.write("=" * 50)
        self.stdout.write("CLASSROOMS IMPORT SUMMARY:")
        self.stdout.write(f"Created: {created_count}")
        self.stdout.write(f"Updated: {updated_count}")
        self.stdout.write(f"Skipped: {skipped_count}")
        self.stdout.write(f"Total classrooms in database: {Classroom.objects.count()}")
        
        # Show classroom distribution by building
        self.stdout.write("\nClassroom distribution by building:")
        from django.db.models import Count
        building_dist = Classroom.objects.values('building').annotate(
            count=Count('id'),
            total_capacity=Count('id')
        ).order_by('building')
        
        for item in building_dist:
            self.stdout.write(f"  {item['building']}: {item['count']} classrooms")