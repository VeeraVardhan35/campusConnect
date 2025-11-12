from django.core.management.base import BaseCommand
from timetable.models import ClassSchedule, Course, Batch, Classroom, TimeSlot
from users.models import User
from django.db import transaction
from datetime import time

class Command(BaseCommand):
    help = 'Populate ClassSchedule for a specific day using professor short names'

    def add_arguments(self, parser):
        parser.add_argument('day', type=str, help='Day of the week (e.g., monday, tuesday)')

    def handle(self, *args, **options):
        day = options['day'].lower()
        
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

    def get_schedule_data(self, day):
        """Return schedule data for the specific day using professor short names"""
        schedules = {
            'monday': [
                # Format: (course_code, batch_year, batch_branch, batch_section, professor_short_name, classroom_number, start_time, end_time)
                
                # Computer Science - A
                ('NS1001', '2025', 'cs', 'A', 'DM', 'L106', '10:00', '11:00'),
                ('ES1002', '2025', 'cs', 'A', 'PKP', 'L106', '11:00', '12:00'),
                ('IT1001', '2025', 'cs', 'A', 'RKS', 'L106', '12:00', '13:00'),
                ('ES1002', '2025', 'cs', 'A', 'PKP', 'ECLab1', '14:00', '16:00'),
                ('NS1002', '2025', 'cs', 'A', 'ACM', 'PhyLab1', '16:00', '18:00'),

                # Computer Science - B
                ('NS1001', '2025', 'cs', 'B', 'NKM', 'L206', '10:00', '11:00'),
                ('HS1001', '2025', 'cs', 'B', 'JAMF', 'L206', '12:00', '13:00'),
                ('IT1001', '2025', 'cs', 'B', 'RKS', 'L206', '11:00', '12:00'),
                ('ES1002', '2025', 'cs', 'B', 'PR', 'L105', '14:00', '15:00'),
                ('ES1002', '2025', 'cs', 'B', 'PR', 'ECLab1', '16:00', '18:00'),

            #     # Electronics & Communication
                ('NS1001', '2025', 'ec', 'A', 'SSL', 'L202', '10:00', '11:00'),
                ('DS1005', '2025', 'ec', 'A', 'JKT', 'L202', '11:00', '12:00'),
                ('HS1001', '2025', 'ec', 'A', 'MA', 'L202', '09:00', '10:00'),
                ('DS1005', '2025', 'ec', 'A', 'JKT', 'L102', '14:00', '16:00'), 
                # bATCH B
                ('NS1001', '2025', 'ec', 'B', 'SSL', 'L202', '10:00', '11:00'),
                ('DS1005', '2025', 'ec', 'B', 'JKT', 'L202', '11:00', '12:00'),
                ('HS1001', '2025', 'ec', 'B', 'MA', 'L202', '09:00', '10:00'),                

                
            #     # Mechanical Engineering
                ('NS1001', '2025', 'me', 'A', 'LKB', 'L102', '10:00', '11:00'),
                ('NS1002', '2023', 'me', 'A', 'YSK', 'PhyLab1', '14:00', '16:00'),
                ('NS1001', '2025', 'me', 'B', 'LKB', 'L102', '10:00', '11:00'),
                ('NS1002', '2025', 'me', 'B', 'YSK', 'PhyLab1', '14:00', '16:00'),
                ('IT1002', '2025', 'me', 'A', 'MKT', 'L201', '17:00', '18:00'),
                ('IT1002', '2025', 'me', 'B', 'MKT', 'L201', '17:00', '18:00'),
                
            #     # Smart Manufacturing
                ('IT1002', '2025', 'sm', 'A', 'RP', 'L201', '16:00', '17:00'),
                ('NS1001', '2025', 'sm', 'A', 'LKB', 'L102', '10:00', '11:00'),
                ('NS1002', '2025', 'sm', 'A', 'YSK', 'PhyLab1', '14:00', '16:00'),
                ('DS1005', '2025', 'sm', 'A', 'AM', 'L102', '17:00', '18:00'),
                ('IT1002', '2025', 'sm', 'A', 'RP', 'L201', '16:00', '17:00'),
                ('NS1001', '2025', 'sm', 'A', 'LKB', 'L102', '10:00', '11:00'),
                ('NS1002', '2025', 'sm', 'A', 'YSK', 'PhyLab1', '14:00', '16:00'),
                ('DS1005', '2025', 'sm', 'A', 'AM', 'L102', '17:00', '18:00'),

                ('OE2N12', 'ALL', 'ALL', '', 'MKP', 'CR107', '12:00', '13:00'),
                ('OE2M07', 'ALL', 'ALL', '', 'CD', 'CR202', '12:00', '13:00'),
                ('OE2CO2', 'ALL', 'ALL', '', 'AO', 'L104', '12:00', '13:00'),
                ('OE2EO1', 'ALL', 'ALL', '', 'KD', 'L207', '12:00', '13:00'),
                ('OE2E03', 'ALL', 'ALL', '', 'AK', 'L201', '12:00', '13:00'),
                ('OE2D11', 'ALL', 'ALL', '', 'VKG', 'L102', '12:00', '13:00'),
                ('IT2001', '2024', 'cs', 'A', 'SKM', 'L104', '10:00', '11:00'),
                ('CS2003', '2024', 'cs', 'B', 'PK', 'L105', '10:00', '11:00'),
                ('EC203',  '2024', 'ec', 'A', '', 'L201', '10:00', '11:00'),
                ('EC203',  '2024', 'ec', 'B', '', 'L201', '10:00', '11:00'),
                ('SM2004', '2024', 'sm', 'A', '', 'CR103', '10:00', '11:00'),
                ('SM2004', '2024', 'sm', 'B', '', 'CR103', '10:00', '11:00'),
                ('IT2002', '2024', 'me', 'A', 'SM', 'CC-GF', '09:00', '11:00'),
                ('IT2002', '2024', 'me', 'B', 'SM', 'CC-GF', '09:00', '11:00'),
                ('CS2003', '2024', 'cs', 'A', 'PK', 'L104', '11:00', '12:00'),
                ('IT2001', '2024', 'cs', 'B', 'SKM', 'L105', '11:00', '12:00'),
                ('ME2004', '2024', 'me', 'A', 'TS', 'CR201', '11:00', '12:00'),
                ('ME2004', '2024', 'me', 'B', 'TS', 'CR201', '11:00', '12:00'),
                ('SM2002', '2024', 'sm', 'A', 'SGM', 'CR103', '11:00', '12:00'),
                ('SM2002', '2024', 'sm', 'B', 'SGM', 'CR103', '11:00', '12:00'),

                ('CS2002', '2024', 'cs', 'A', 'RKR', 'L106', '14:00', '15:00'),
                ('CS2004', '2024', 'cs', 'B', 'AP', 'L206', '14:00', '15:00'),
                ('EC204',  '2024', 'ec', 'A', 'PNK', 'L201', '14:00', '15:00'),
                ('EC204',  '2024', 'ec', 'B', 'PNK', 'L201', '14:00', '15:00'),

                ('CS2004', '2024', 'cs', 'A', 'AP', 'L106', '15:00', '16:00'),
                ('CS2002', '2024', 'cs', 'B', 'RKR', 'L206', '15:00', '16:00'),

                ('ME2003', '2024', 'me', 'A', 'VKG', 'MechLab1', '14:00', '16:00'),
                ('ME2003', '2024', 'me', 'B', 'VKG', 'MechLab1', '14:00', '16:00'),

                ('IT2S01', '2024', 'sm', 'A', 'DSR', 'CC-GF', '14:00', '17:00'),
                ('IT2S01', '2024', 'sm', 'B', 'DSR', 'CC-GF', '14:00', '17:00'),

                ('SM2003', '2024', 'sm', 'A', 'SDP', 'CR103', '17:00', '18:00'),
                ('SM2003', '2024', 'sm', 'B', 'SDP', 'CR103', '17:00', '18:00'),
                ('CS3010', '2023', 'cs', 'A', 'AG', 'CC-SF', '09:00', '11:00'),
                ('SM3009', '2023', 'sm', 'A', 'KP', 'CR201', '09:00', '10:00'),
                ('SM3009', '2023', 'sm', 'B', 'KP', 'CR201', '09:00', '10:00'),
                ('CS3010', '2023', 'cs', 'B', 'AG', 'CC-SF', '11:00', '13:00'),
                ('EC3011', '2023', 'ec', 'A', 'MDB', 'L107', '11:00', '12:00'),
                ('EC3011', '2023', 'ec', 'B', 'MDB', 'L107', '11:00', '12:00'),
                ('ME3010', '2023', 'me', 'A', 'MZA', 'CR103', '12:00', '13:00'),
                ('ME3010', '2023', 'me', 'B', 'MZA', 'CR103', '12:00', '13:00'),
                ('SM3010', '2023', 'sm', 'A', 'ARR', 'CC-GF', '11:00', '13:00'),
                ('SM3010', '2023', 'sm', 'B', 'ARR', 'CC-GF', '11:00', '13:00'),

                ('CS3009', '2023', 'cs', 'A', 'ShM', 'L104', '14:00', '15:00'),
                ('ME3009', '2023', 'me', 'A', 'AM', 'CR201', '14:00', '15:00'),
                ('ME3009', '2023', 'me', 'B', 'AM', 'CR201', '14:00', '15:00'),
                ('SM3012', '2023', 'sm', 'A', 'SA', 'CPPSLab', '14:00', '16:00'),

                ('CS3009', '2023', 'cs', 'B', 'ShM', 'L105', '15:00', '16:00'),
                ('EC3009', '2023', 'ec', 'A', 'DPS', 'L207', '15:00', '16:00'),
                ('EC3009', '2023', 'ec', 'B', 'DPS', 'L207', '15:00', '16:00'),

                ('CS3011', '2023', 'cs', 'A', 'DS', 'L104', '16:00', '17:00'),
                ('CS8028', '2023', 'cs', 'A', 'BA', 'L105', '16:00', '17:00'),
                ('CS8028', '2023', 'cs', 'B', 'BA', 'L105', '16:00', '17:00'),
                ('EC3010', '2023', 'ec', 'A', 'TK', 'L107', '16:00', '17:00'),
                ('EC3010', '2023', 'ec', 'B', 'TK', 'L107', '16:00', '17:00'),

                ('ME3010', '2023', 'me', 'A', 'MZA', 'CPPSLab', '16:00', '18:00'),
                ('ME3010', '2023', 'me', 'B', 'MZA', 'CPPSLab', '16:00', '18:00'),
                ('EC5015', '2022', 'ALL', 'ALL', 'TK', 'CR108', '09:00', '10:00'),
                ('EC8030', '2022', 'ALL', 'ALL', 'PR', 'CR109', '09:00', '10:00'),
                ('CS8004', '2022', 'ALL', 'ALL', 'AO', 'L206', '09:00', '10:00'),

                ('EC5M02', '2022', 'ALL', '', 'SNS', 'CR104', '11:00', '13:00'),
                ('ME8033', '2022', 'me', 'B', 'PT', 'CC-GF', '11:00', '13:00'),
                ('CS8037', '2022', 'cs', 'A', 'ChS', 'CR108', '14:00', '15:00'),
                ('CS8037', '2022', 'cs', 'B', 'ChS', 'CR108', '14:00', '15:00'),
                ('OEM35',  '2022', 'ALL', 'ALL', 'RP', 'CR104', '14:00', '15:00'),
                ('ME8032', '2022', 'ALL', '', 'SGM', 'CR102', '14:00', '15:00'),

                ('ME8016', '2022', 'ALL', 'ALL', 'HSN', 'CR103', '15:00', '16:00'),
                ('OE4M52', '2022', 'ALL', 'ALL', 'KP',  'CR101', '15:00', '16:00'),
                ('EC8004', '2022', 'ALL', 'ALL', 'AV',  'CR108', '15:00', '16:00'),
                ('EC5016', '2022', 'ALL', 'ALL', 'DKV', 'CR102', '15:00', '16:00'),
                ('CS8018', '2022', 'ALL', 'ALL', 'ACP', 'L107',  '15:00', '16:00'),
                ('CS8013', '2022', 'ALL', 'ALL', 'VKJ', 'CR202', '15:00', '16:00'),

                ('EC5C01', '2022', 'ALL', 'ALL', 'MDB', 'CR102', '16:00', '17:00'),
                ('DC5N01', '2022', 'ALL', 'ALL', 'PNK', 'CR103', '16:00', '17:00'),
                ('CS8007', '2022', 'ALL', 'ALL', 'AnS', 'L106',  '16:00', '17:00'),
                ('ME8033', '2022', 'ALL', 'ALL', 'PT',  'CR101', '16:00', '17:00'),
                ('ME8002', '2022', 'ALL', 'ALL', 'MS',  'CR104', '16:00', '17:00'),

                ('ME8031', '2022', 'ALL', 'ALL', 'CD',  'CR201', '17:00', '18:00'),
                ('OE4M76', '2022', 'ALL', 'ALL', 'SKS', 'L202',  '17:00', '18:00'),
                ('EC5M03', '2022', 'ALL', 'ALL', 'AK',  'CR102', '17:00', '18:00'),
                ('CS8025', '2022', 'ALL', 'ALL', 'AS',  'L106',  '17:00', '18:00'),
                ('OE4L73', '2022', 'ALL', 'ALL', 'JAMF', 'CR107', '17:00', '18:00'),
                ('NP8002', '2022', 'ALL', 'ALL', 'NKJ', 'CR202', '17:00', '18:00'),



            ],
            #     # Common Courses
            #     ('NS1001', '2023', 'cs', 'A', 'JA', '501', '08:00', '09:00'),
            #     ('NS1001', '2023', 'ec', 'A', 'JA', '502', '08:00', '09:00'),
            # ],
            # 'tuesday': [
            #     # Computer Science
            #     ('CS2004', '2023', 'cs', 'A', 'JT', '101', '09:00', '10:00'),
            #     ('CS3010', '2023', 'cs', 'A', 'MJ', '102', '10:00', '11:00'),
                
            #     # Electronics & Communication
            #     ('EC3010', '2023', 'ec', 'A', 'DW', '201', '09:00', '10:00'),
            #     ('EC3011', '2023', 'ec', 'A', 'PH', '202', '14:00', '15:00'),
                
            #     # Mechanical Engineering
            #     ('ME2002', '2023', 'me', 'A', 'CM', '301', '10:00', '11:00'),
                
            #     # Smart Manufacturing
            #     ('SM3000', '2023', 'sm', 'A', 'AS', '401', '11:00', '12:00'),
                
            #     # Common Courses
            #     ('HS1001', '2023', 'cs', 'A', 'RS', '501', '16:00', '17:00'),
            #     ('HS1001', '2023', 'ec', 'A', 'RS', '502', '16:00', '17:00'),
            # ],
            'wednesday': [
                    ('HS1001', '2025', 'sm', 'A', 'MA', 'L102', '09:00', '10:00'),
                    ('HS1001', '2025', 'sm', 'B', 'MA', 'L102', '09:00', '10:00'),
                    ('HS1001', '2025', 'me', 'A', 'MA', 'L102', '09:00', '10:00'),
                    ('HS1001', '2025', 'me', 'B', 'MA', 'L102', '09:00', '10:00'),


                    ('NS1001', '2025', 'cs', 'A', 'DM', 'L106', '10:00', '11:00'),
                    ('NS1001', '2025', 'cs', 'B', 'NKM', 'L206', '10:00', '11:00'),
                    ('NS1001', '2025', 'ec', 'A', 'SSL', 'L202', '10:00', '11:00'),
                    ('NS1001', '2025', 'ec', 'B', 'SSL', 'L202', '10:00', '11:00'),

                    ('ES1002', '2025', 'cs', 'A', 'PKP', 'L106', '11:00', '12:00'),
                    ('ES1002', '2025', 'cs', 'B', 'PR',  'L206', '11:00', '12:00'),
                    ('HS1001', '2025', 'ec', 'A', 'MA', 'L202', '11:00', '12:00'),
                    ('HS1001', '2025', 'ec', 'B', 'MA', 'L202', '11:00', '12:00'),

                    ('IT1002', '2025', 'ec', 'A', 'AV', 'L202', '12:00', '13:00'),
                    ('IT1002', '2025', 'ec', 'B', 'AV', 'L202', '12:00', '13:00'),
                    ('DS1005', '2025', 'sm', 'A', '', 'L102', '12:00', '13:00'),
                    ('DS1005', '2025', 'sm', 'B', '', 'L102', '12:00', '13:00'),

                    ('HS1001', '2025', 'cs', 'A', 'JAMF', 'L206', '14:00', '15:00'),
                    ('DS1005', '2025', 'ec', 'A', 'JKT', 'L201', '14:00', '15:00'),
                    ('DS1005', '2025', 'ec', 'B', 'JKT', 'L201', '14:00', '15:00'),

                    ('ES1002', '2025', 'cs', 'B', 'PR',  'ECLab', '14:00', '16:00'),
                    ('ES1002', '2025', 'cs', 'A', 'PKP', 'ECLab', '16:00', '18:00'),

                    ('IT1002', '2025', 'me', 'A', 'MKT', 'CC-GF', '15:00', '18:00'),
                    ('IT1002', '2025', 'me', 'B', 'MKT', 'CC-GF', '15:00', '18:00'),

                    ('DS1005', '2024', 'sm', 'A', 'MKT', 'CC-GF', '15:00', '18:00'),
                    ('DS1005', '2024', 'sm', 'B', 'MKT', 'CC-GF', '15:00', '18:00'),
                    ('CS2002', '2024', 'cs', 'B', 'RKR', 'L105', '09:00', '10:00'),
                    ('IT2002', '2024', 'ec', 'A', 'GF', 'L201', '09:00', '10:00'),
                    ('IT2002', '2024', 'ec', 'B', 'GF', 'L201', '09:00', '10:00'),
                    ('IT2002', '2024', 'sm', 'A', 'RKS', 'L202', '09:00', '10:00'),
                    ('IT2002', '2024', 'sm', 'B', 'RKS', 'L202', '09:00', '10:00'),
                    ('IT2002', '2024', 'me', 'A', 'RKS', 'L202', '09:00', '10:00'),
                    ('IT2002', '2024', 'me', 'B', 'RKS', 'L202', '09:00', '10:00'),

                    ('IT2C01', '2024', 'cs', 'A', 'AS', 'CC-GF', '09:00', '12:00'),

                    ('CS2002', '2024', 'cs', 'B', 'RKR', 'L105', '10:00', '11:00'),
                    ('EC204',  '2024', 'ec', 'A', 'PNK', 'L201', '10:00', '11:00'),
                    ('EC204',  '2024', 'ec', 'B', 'PNK', 'L201', '10:00', '11:00'),
                    ('SM2004', '2024', 'sm', 'A', 'TC', 'CR104', '10:00', '11:00'),
                    ('SM2004', '2024', 'sm', 'B', 'TC', 'CR104', '10:00', '11:00'),

                    ('CS2003', '2024', 'cs', 'B', 'PK', 'L105', '11:00', '12:00'),
                    ('IT2M01', '2024', 'me', 'A', 'DSR', 'CC-GF', '10:00', '13:00'),
                    ('IT2M01', '2024', 'me', 'B', 'DSR', 'CC-GF', '10:00', '13:00'),
                    ('IT2002', '2024', 'ec', 'A', 'VF', 'CC-GF', '11:00', '12:00'),
                    ('IT2002', '2024', 'ec', 'B', 'VF', 'CC-GF', '11:00', '12:00'),

                    ('CS2003', '2024', 'cs', 'A', 'PK', 'L104', '12:00', '13:00'),
                    ('IT2001', '2024', 'cs', 'B', 'SKM', 'L105', '12:00', '13:00'),

                    ('CS2002', '2024', 'cs', 'A', 'RKR', 'L105', '14:00', '15:00'),
                    ('EC2002', '2024', 'ec', 'A', 'PS', 'L202', '14:00', '15:00'),
                    ('EC2002', '2024', 'ec', 'B', 'PS', 'L202', '14:00', '15:00'),
                    ('ME2002', '2024', 'me', 'A', 'MS', 'CR102', '14:00', '15:00'),
                    ('ME2002', '2024', 'me', 'B', 'MS', 'CR102', '14:00', '15:00'),

                    ('IT2001', '2024', 'cs', 'A', 'SKM', 'L105', '15:00', '16:00'),
                    ('EC203',  '2024', 'ec', 'A', 'SKT', 'L202', '15:00', '16:00'),
                    ('EC203',  '2024', 'ec', 'B', 'SKT', 'L202', '15:00', '16:00'),
                    ('SM2002', '2024', 'sm', 'A', 'SGM', 'PHYLaB', '14:00', '16:00'),

                    ('IT2001', '2024', 'ec', 'A', 'VF', 'CC-GF', '16:00', '18:00'),
                    ('IT2001', '2024', 'ec', 'B', 'VF', 'CC-GF', '16:00', '18:00'),

                    ('ME2003', '2024', 'me', 'A', 'VKG', 'CR101', '16:00', '17:00'),
                    ('ME2003', '2024', 'me', 'B', 'VKG', 'CR101', '16:00', '17:00'),

                    ('NS2001', '2024', 'cs', 'A', 'VF', 'L202', '17:00', '18:00'),

                    ('IT2002', '2024', 'sm', 'A', 'RKS', 'L102', '17:00', '18:00'),
                    ('IT2002', '2024', 'sm', 'B', 'RKS', 'L102', '17:00', '18:00'),
                    ('IT2002', '2024', 'me', 'A', 'RKS', 'L102', '17:00', '18:00'),
                    ('IT2002', '2024', 'me', 'B', 'RKS', 'L102', '17:00', '18:00'),
                    ('IT3E01', '2023', 'ec', 'A', 'KD', 'VLSILab', '09:00', '12:00'),
                    ('IT3E01', '2023', 'ec', 'B', 'KD', 'VLSILab', '09:00', '12:00'),

                    ('ME3011', '2023', 'me', 'A', 'SKC', 'CR102', '10:00', '11:00'),
                    ('ME3011', '2023', 'me', 'B', 'SKC', 'CR102', '10:00', '11:00'),
                    ('SM3011', '2023', 'sm', 'A', 'TS',  'CR201', '10:00', '11:00'),
                    ('SM3011', '2023', 'sm', 'B', 'TS',  'CR201', '10:00', '11:00'),

                    ('SM3009', '2023', 'sm', 'A', 'KP', 'CR103', '11:00', '12:00'),
                    ('SM3009', '2023', 'sm', 'B', 'KP', 'CR103', '11:00', '12:00'),

                    ('OE3M27', '2023', 'ALL', 'ALL', 'SM',  'CR201', '12:00', '13:00'),
                    ('OE2M10', '2023', 'ALL', 'ALL', 'TC',  'CR202', '12:00', '13:00'),
                    ('OE3E40', '2023', 'ALL', 'ALL', 'SNS', 'CR109', '12:00', '13:00'),
                    ('OE4E50', '2023', 'ALL', 'ALL', 'SKT', 'L207',  '12:00', '13:00'),
                    ('EC8049', '2023', 'ALL', 'ALL', 'KD',  'CR104', '12:00', '13:00'),
                    ('OE3N38', '2023', 'ALL', 'ALL', 'NRJ', 'CR102', '12:00', '13:00'),
                    ('CS8016', '2023', 'ALL', 'ALL', 'VMa', 'CR107', '12:00', '13:00'),

                    ('CS3009', '2023', 'cs', 'A', 'ShM', 'L104', '14:00', '15:00'),
                    ('CS3010', '2023', 'cs', 'B', 'AG',  'L106', '14:00', '15:00'),
                    ('SM3010', '2023', 'sm', 'A', 'ARR', 'CR201', '14:00', '15:00'),
                    ('SM3010', '2023', 'sm', 'B', 'ARR', 'CR201', '14:00', '15:00'),

                    ('CS3010', '2023', 'cs', 'A', 'AG',  'L104', '15:00', '16:00'),
                    ('CS3009', '2023', 'cs', 'B', 'ShM', 'L106', '15:00', '16:00'),

                    ('IT3E01', '2023', 'ec', 'A', 'KD', 'VLSILab', '14:00', '17:00'),
                    ('IT3E01', '2023', 'ec', 'B', 'KD', 'VLSILab', '14:00', '17:00'),

                    ('SM3012', '2023', 'sm', 'B', 'SA', 'CPPSLab', '15:00', '17:00'),

                    ('CS3011', '2023', 'cs', 'A', 'DS', 'L104', '16:00', '17:00'),




            ],
            # 'thursday': [
            #     # Computer Science
            #     ('CS3028', '2023', 'cs', 'A', 'VP', '101', '09:00', '10:00'),
            #     ('CS3016', '2023', 'cs', 'A', 'SK', '102', '10:00', '11:00'),
                
            #     # Electronics & Communication
            #     ('OE2001', '2023', 'ec', 'A', 'KD', '201', '11:00', '12:00'),
            #     ('OE2003', '2023', 'ec', 'A', 'AK', '202', '14:00', '15:00'),
                
            #     # Mechanical Engineering
            #     ('ME3010', '2023', 'me', 'A', 'MZ', '301', '15:00', '16:00'),
            #     ('ME3011', '2023', 'me', 'A', 'AR', '302', '16:00', '17:00'),
                
            #     # Smart Manufacturing
            #     ('SM3011', '2023', 'sm', 'A', 'TS', '401', '10:00', '11:00'),
            # ],
            # 'friday': [
            #     # Computer Science
            #     ('CS3111', '2023', 'cs', 'A', 'ND', '101', '09:00', '10:00'),
            #     ('CS3113', '2023', 'cs', 'A', 'AC', '102', '10:00', '11:00'),
                
            #     # Electronics & Communication
            #     ('EC3000', '2023', 'ec', 'A', 'PR', '201', '11:00', '12:00'),
                
            #     # Mechanical Engineering
            #     ('ME3000', '2023', 'me', 'A', 'DS', '301', '14:00', '15:00'),
                
            #     # Smart Manufacturing
            #     ('CS3001', '2023', 'sm', 'A', 'MD', '401', '15:00', '16:00'),
                
            #     # Common Electives
            #     ('OE2007', '2023', 'me', 'A', 'SK', '501', '16:00', '17:00'),
            #     ('OE2008', '2023', 'sm', 'A', 'SA', '502', '16:00', '17:00'),
            # ],
            # 'saturday': [
            #     # Extra Labs and Tutorials
            #     ('IT1001', '2023', 'cs', 'A', 'SJ', 'Lab-101', '09:00', '11:00'),
            #     ('EC2002', '2023', 'ec', 'A', 'RW', 'Lab-201', '11:00', '13:00'),
            #     ('ME2002', '2023', 'me', 'A', 'CM', 'Lab-301', '14:00', '16:00'),
                
            #     # Project Work
            #     ('CS2005', '2023', 'cs', 'A', 'MB', '103', '16:00', '18:00'),
        }
        
        return schedules.get(day, [])

    def create_class_schedule(self, schedule_data, day):
        """Create a single class schedule using professor short name"""
        try:
            (course_code, batch_year, batch_branch, batch_section, 
             professor_short_name, classroom_number, start_time_str, end_time_str) = schedule_data

            # Convert time strings to time objects
            start_time = time(*map(int, start_time_str.split(':')))
            end_time = time(*map(int, end_time_str.split(':')))

            # Get objects
            course = Course.objects.get(code=course_code)
            batch = Batch.objects.get(
                batch_year=batch_year,
                branch=batch_branch, 
                section=batch_section
            )
            
            # Get professor by short name
            professor = User.objects.get(short_name=professor_short_name, role='professor')
            
            classroom = Classroom.objects.get(room_number=classroom_number)
            
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

        except Course.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"✗ Course not found: {course_code}"))
        except Batch.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"✗ Batch not found: {batch_year} {batch_branch} {batch_section}"))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"✗ Professor not found with short name: {professor_short_name}"))
        except Classroom.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"✗ Classroom not found: {classroom_number}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Error: {e}"))

        return False

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