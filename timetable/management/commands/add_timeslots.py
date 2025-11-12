from django.core.management.base import BaseCommand
from timetable.models import TimeSlot
from datetime import time

class Command(BaseCommand):
    help = 'Populate TimeSlot table with class timings from 8:00 AM to 6:00 PM'

    def handle(self, *args, **options):
        # Define days of the week
        days = [
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
        ]

        # Define time slots (start_time, end_time) - 1 hour each
        time_slots = [
            # Morning sessions
            (time(8, 0), time(9, 0)),   # 8:00 AM - 9:00 AM
            (time(9, 0), time(10, 0)),  # 9:00 AM - 10:00 AM
            (time(10, 0), time(11, 0)), # 10:00 AM - 11:00 AM
            (time(11, 0), time(12, 0)), # 11:00 AM - 12:00 PM
            
            # Afternoon sessions
            (time(12, 0), time(13, 0)), # 12:00 PM - 1:00 PM
            (time(13, 0), time(14, 0)), # 1:00 PM - 2:00 PM
            (time(14, 0), time(15, 0)), # 2:00 PM - 3:00 PM
            (time(15, 0), time(16, 0)), # 3:00 PM - 4:00 PM
            (time(16, 0), time(17, 0)), # 4:00 PM - 5:00 PM
            (time(17, 0), time(18, 0)), # 5:00 PM - 6:00 PM
        ]

        created_count = 0
        updated_count = 0

        self.stdout.write("Populating TimeSlot table...")
        self.stdout.write("=" * 50)

        for day_code, day_name in days:
            self.stdout.write(f"\n{day_name}:")
            self.stdout.write("-" * 30)
            
            for start_time, end_time in time_slots:
                # Create display name for the time slot
                display_name = f"{day_name} {start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"
                
                try:
                    # Try to get existing time slot or create new one
                    time_slot, created = TimeSlot.objects.update_or_create(
                        day=day_code,
                        start_time=start_time,
                        end_time=end_time,
                        defaults={
                            'day': day_code,
                            'start_time': start_time,
                            'end_time': end_time
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ Created: {display_name}")
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f"  ↻ Updated: {display_name}")
                        )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"  ✗ Failed: {display_name} - Error: {e}")
                    )

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("TIMESLOT POPULATION SUMMARY:")
        self.stdout.write("=" * 50)
        
        self.stdout.write(f"\nTime Slots Created: {created_count}")
        self.stdout.write(f"Time Slots Updated: {updated_count}")
        self.stdout.write(f"Total Time Slots: {TimeSlot.objects.count()}")
        
        # Show breakdown by day
        self.stdout.write(f"\nBreakdown by Day:")
        for day_code, day_name in days:
            day_count = TimeSlot.objects.filter(day=day_code).count()
            self.stdout.write(f"  {day_name}: {day_count} time slots")
        
        # Show sample time slots
        self.stdout.write(f"\nSample Time Slots:")
        self.stdout.write("-" * 30)
        sample_slots = TimeSlot.objects.all().order_by('day', 'start_time')[:6]
        for slot in sample_slots:
            self.stdout.write(f"  {slot}")

        self.stdout.write(
            self.style.SUCCESS(f"\n✅ TimeSlot population completed successfully!")
        )