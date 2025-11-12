from django.core.management.base import BaseCommand
from timetable.models import Course

class Command(BaseCommand):
    help = 'Add all courses from the PDF to the database'

    def handle(self, *args, **options):
        courses_data = [
            # Computer Science (CSE) Courses
            {'code': 'NS1001', 'name': 'Mathematics-I', 'credits': 4, 'discipline': 'Common'},
            {'code': 'NS1002', 'name': 'Engineering Mechanics', 'credits': 4, 'discipline': 'Common'},
            {'code': 'IT1001', 'name': 'Introduction to Programming In C', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'ES1002', 'name': 'Fundamentals of Electrical and Electronics Engineering', 'credits': 4, 'discipline': 'CSE'},
            {'code': 'CS1001', 'name': 'Introduction to Professional', 'credits': 1, 'discipline': 'CSE'},
            {'code': 'IT2001', 'name': 'Data Structure in C', 'credits': 4, 'discipline': 'CSE'},
            {'code': 'CS2000', 'name': 'Computer Organisation and Architecture', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'CS2003', 'name': 'Database Management Systems', 'credits': 4, 'discipline': 'CSE'},
            {'code': 'CS2004', 'name': 'Introduction to Data Science', 'credits': 4, 'discipline': 'CSE'},
            {'code': 'CS2005', 'name': 'Course Structure', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'CS3000', 'name': 'Network Security & Cryptography', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'CS3010', 'name': 'Software Engineering', 'credits': 4, 'discipline': 'CSE'},
            {'code': 'CS3011', 'name': 'Artificial Intelligence', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'CS3028', 'name': 'Hardware Security', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'CS3016', 'name': 'Cloud Computing', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'CS3111', 'name': 'Cyber Security', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'CS3113', 'name': 'Web Mining', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'CS3114', 'name': 'Mobile and Wireless Networks', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'CS3122', 'name': 'Soft Computing', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'CS3204', 'name': 'Deep Learning and Applications', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'CS3207', 'name': 'Social Network Analysis', 'credits': 3, 'discipline': 'CSE'},
            {'code': 'CS3125', 'name': 'Fuzzy Sets, Logic and Applications', 'credits': 3, 'discipline': 'CSE'},

            # Electronics & Communication (ECE) Courses
            {'code': 'IT1002', 'name': 'Introduction to Programming in Python', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'EC1001', 'name': 'Introduction to Professional', 'credits': 1, 'discipline': 'ECE'},
            {'code': 'IT2002', 'name': 'Data Structure in Python', 'credits': 4, 'discipline': 'ECE'},
            {'code': 'EC2002', 'name': 'Digital Electronics and Microprocessor Interfaces', 'credits': 4, 'discipline': 'ECE'},
            {'code': 'EC2003a', 'name': 'Principle of Analog Communications', 'credits': 2, 'discipline': 'ECE'},
            {'code': 'EC2003b', 'name': 'Network Theory (Analysis and Synthesis)', 'credits': 2, 'discipline': 'ECE'},
            {'code': 'EC2004a', 'name': 'Electronic Devices and Circuits', 'credits': 2, 'discipline': 'ECE'},
            {'code': 'EC2004b', 'name': 'Instrumentation and Measurement', 'credits': 2, 'discipline': 'ECE'},
            {'code': 'OE2001', 'name': 'Introduction to Sensors and Actuators', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'OE2003', 'name': 'Fundamentals of Signals and Systems', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'EC3000', 'name': 'VLS System Design (VLSI IC design, logic synthesis using VHDL)', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'EC3010', 'name': 'Fundamentals of Electromagnetic Theory', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'EC3011', 'name': 'Digital Communications', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'OE3540', 'name': 'Computation Genomic & Proteomic', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'OE4540', 'name': 'Detection and Estimation Theory', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'EC0039', 'name': 'Advanced Digital Filter Design', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'OE4575', 'name': 'Advance Antenna Theory Design', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'EC5030', 'name': 'CMOS Memory Design', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'EC5034', 'name': 'Pattern Recognition and Machine Learning', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'OE4569', 'name': 'Optical Communication', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'EC50206', 'name': 'Photovoltaics: Fundamentals and Applications', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'EC5040', 'name': 'Wireless Communications', 'credits': 3, 'discipline': 'ECE'},
            {'code': 'EC50401', 'name': 'Physics of Semiconductor Devices', 'credits': 3, 'discipline': 'ECE'},

            # Mechanical Engineering (ME) Courses
            {'code': 'ME1001', 'name': 'Introduction to Professional', 'credits': 1, 'discipline': 'ME'},
            {'code': 'DS1005', 'name': 'Engineering Graphics', 'credits': 3, 'discipline': 'ME'},
            {'code': 'ME2002', 'name': 'Manufacturing Process', 'credits': 4, 'discipline': 'ME'},
            {'code': 'ME2003', 'name': 'Solid Mechanics', 'credits': 4, 'discipline': 'ME'},
            {'code': 'ME2004', 'name': 'Engineering Thermodynamics', 'credits': 4, 'discipline': 'ME'},
            {'code': 'OE2007', 'name': 'Operations Research', 'credits': 3, 'discipline': 'ME'},
            {'code': 'ME3000', 'name': 'Design of Mechanical Components', 'credits': 3, 'discipline': 'ME'},
            {'code': 'ME3010', 'name': 'Industrial Internet of Things', 'credits': 3, 'discipline': 'ME'},
            {'code': 'ME3011', 'name': 'Heat Transfer', 'credits': 4, 'discipline': 'ME'},
            {'code': 'OE4545', 'name': 'Computer-Aided Design (CAD)', 'credits': 3, 'discipline': 'ME'},
            {'code': 'OEM473', 'name': 'Fundamentals of Tribology & Rheology', 'credits': 3, 'discipline': 'ME'},
            {'code': 'ME5003', 'name': 'Finite Element Methods for Mechanical Engineering', 'credits': 3, 'discipline': 'ME'},
            {'code': 'OEM476', 'name': 'Digital Twins in Manufacturing', 'credits': 3, 'discipline': 'ME'},
            {'code': 'ME5002', 'name': 'Mechanical Vibrations and Condition Monitoring', 'credits': 3, 'discipline': 'ME'},
            {'code': 'OEM455', 'name': 'Advanced Manufacturing Processes and Technologies', 'credits': 3, 'discipline': 'ME'},
            {'code': 'ME5016', 'name': 'Biomaterials Science and Engineering', 'credits': 3, 'discipline': 'ME'},
            {'code': 'OEM452', 'name': 'Rapid Product Development Technologies', 'credits': 3, 'discipline': 'ME'},
            {'code': 'OEM422', 'name': 'Industrial Instrumentation & Metrology', 'credits': 3, 'discipline': 'ME'},
            {'code': 'ME5010', 'name': 'MEMS: Microfabrication and Application', 'credits': 3, 'discipline': 'ME'},
            {'code': 'ME5021', 'name': 'Computer Aided Geometric Design', 'credits': 3, 'discipline': 'ME'},
            {'code': 'ME5022', 'name': 'Design for Experiments', 'credits': 3, 'discipline': 'ME'},

            # Smart Manufacturing (SM) Courses
            {'code': 'SM1001', 'name': 'Introduction to Professional', 'credits': 1, 'discipline': 'SM'},
            {'code': 'SM2002', 'name': 'Manufacturing Process', 'credits': 4, 'discipline': 'SM'},
            {'code': 'SM2003', 'name': 'Solid Mechanics - Design of Mechanical Components', 'credits': 4, 'discipline': 'SM'},
            {'code': 'SM2004', 'name': 'Engineering Thermodynamics + Heat Transfer', 'credits': 4, 'discipline': 'SM'},
            {'code': 'OE2008', 'name': 'Probabilistic Approaches to Machine Learning', 'credits': 3, 'discipline': 'SM'},
            {'code': 'SM3000', 'name': 'Additive and Subtractive Manufacturing Processes', 'credits': 3, 'discipline': 'SM'},
            {'code': 'SM3010', 'name': 'Computer Aided Product Development', 'credits': 3, 'discipline': 'SM'},
            {'code': 'SM3011', 'name': 'Industrial Automation', 'credits': 3, 'discipline': 'SM'},
            {'code': 'CS3001', 'name': 'Advanced Cyber Physical System', 'credits': 3, 'discipline': 'SM'},
            {'code': 'OE4546', 'name': 'Business Analytics using R', 'credits': 3, 'discipline': 'SM'},
            {'code': 'MTX003', 'name': 'Advances in Sensors and Actuators', 'credits': 3, 'discipline': 'SM'},
            {'code': 'OEM474', 'name': 'AI and ML for Engineering', 'credits': 3, 'discipline': 'SM'},

            # Design (DS) Courses
            {'code': 'DS1000', 'name': 'Design Fundamentals 1', 'credits': 3, 'discipline': 'DS'},
            {'code': 'DS1003', 'name': 'Design Drawing', 'credits': 2, 'discipline': 'DS'},
            {'code': 'DS1004', 'name': 'Representation Technique', 'credits': 3, 'discipline': 'DS'},
            {'code': 'DS1001', 'name': 'Introduction to Professional', 'credits': 1, 'discipline': 'DS'},
            {'code': 'DS2005', 'name': 'Studies in Form', 'credits': 3, 'discipline': 'DS'},
            {'code': 'DS2006', 'name': 'Industrial Design 1', 'credits': 3, 'discipline': 'DS'},
            {'code': 'DS2007', 'name': 'Communication Design 1', 'credits': 3, 'discipline': 'DS'},
            {'code': 'DS2008', 'name': 'Design Project 1', 'credits': 3, 'discipline': 'DS'},
            {'code': 'DS2010', 'name': 'Material and Processes', 'credits': 3, 'discipline': 'DS'},
            {'code': 'DS3021', 'name': 'Engineering Design - Including Design and Fabrication Project', 'credits': 4, 'discipline': 'DS'},
            {'code': 'OE4516', 'name': 'Visual Ergonomics', 'credits': 3, 'discipline': 'DS'},
            {'code': 'DS3031', 'name': 'Engineering Design - Including Design and Fabrication Project', 'credits': 4, 'discipline': 'DS'},
            {'code': 'DS3032', 'name': 'Service Design', 'credits': 3, 'discipline': 'DS'},
            {'code': 'DS3010', 'name': 'Sustainable Design', 'credits': 3, 'discipline': 'DS'},
            {'code': 'DS3011', 'name': 'Design Management', 'credits': 3, 'discipline': 'DS'},
            {'code': 'DS3012', 'name': 'Design Project 4', 'credits': 5, 'discipline': 'DS'},
            {'code': 'DS4013', 'name': 'Design Seminar I', 'credits': 3, 'discipline': 'DS'},
            {'code': 'DS4014', 'name': 'Design Thesis II', 'credits': 14, 'discipline': 'DS'},

            # Common & Interdisciplinary Courses
            {'code': 'HS1001', 'name': 'Effective Communications', 'credits': 2, 'discipline': 'Common'},
            {'code': 'ES1003', 'name': 'Innovation Theory and Practice', 'credits': 2, 'discipline': 'Common'},
            {'code': 'PC1001', 'name': 'Professional Development Course', 'credits': 1, 'discipline': 'Common'},
            {'code': 'NG2001', 'name': 'Biology for Engineers', 'credits': 2, 'discipline': 'Common'},
            {'code': 'OE2012', 'name': 'Numerical Methods for Engineers', 'credits': 3, 'discipline': 'Common'},
            {'code': 'OE2013', 'name': 'Semiconductor Optoelectronic Devices', 'credits': 3, 'discipline': 'Common'},
            {'code': 'OE2014', 'name': 'SCIENCE AND CULTURE - A COMPARISON', 'credits': 3, 'discipline': 'Common'},
            {'code': 'PRO202', 'name': 'Discipline Project', 'credits': 2, 'discipline': 'Common'},
            {'code': 'PC2020', 'name': 'Professional Development Course', 'credits': 1, 'discipline': 'Common'},
            {'code': 'HS3024', 'name': 'Ecology & Environment Science', 'credits': 2, 'discipline': 'Common'},
            {'code': 'PRO203', 'name': 'Optional Project', 'credits': 2, 'discipline': 'Common'},
            {'code': 'PC3003', 'name': 'Professional Development Course', 'credits': 1, 'discipline': 'Common'},
            {'code': 'OEM777', 'name': 'Nano technology for Engineers', 'credits': 3, 'discipline': 'Common'},
            {'code': 'OEM73', 'name': 'LIFE SKILLS MANAGEMENT', 'credits': 3, 'discipline': 'Common'},
            {'code': 'PC4004', 'name': 'Professional Development Course', 'credits': 1, 'discipline': 'Common'},
        ]

        created_count = 0
        updated_count = 0
        skipped_count = 0

        self.stdout.write("Adding courses to database...")
        self.stdout.write("=" * 60)

        # Group by discipline for better reporting
        disciplines = {}
        for course_data in courses_data:
            discipline = course_data.get('discipline', 'Unknown')
            if discipline not in disciplines:
                disciplines[discipline] = []
            disciplines[discipline].append(course_data)

        for discipline, disc_courses in disciplines.items():
            self.stdout.write(f"\n{discipline} Courses:")
            self.stdout.write("-" * 40)
            
            for course_data in disc_courses:
                code = course_data['code']
                name = course_data['name']
                credits = course_data['credits']
                discipline_name = course_data['discipline']

                # Skip if course code is invalid
                if code == 'NEW' or not code.strip():
                    skipped_count += 1
                    self.stdout.write(
                        self.style.WARNING(f"  ✗ Skipped (Invalid code): {code}")
                    )
                    continue

                try:
                    # Try to get existing course or create new one
                    course, created = Course.objects.update_or_create(
                        code=code,
                        defaults={
                            'name': name,
                            'credits': credits
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ Created: {code} - {name}")
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f"  ↻ Updated: {code} - {name}")
                        )

                except Exception as e:
                    skipped_count += 1
                    self.stdout.write(
                        self.style.ERROR(f"  ✗ Failed: {code} - {name} - Error: {e}")
                    )

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("COURSES IMPORT SUMMARY:")
        self.stdout.write("=" * 60)
        
        # Discipline-wise breakdown
        self.stdout.write("\nDiscipline Breakdown:")
        for discipline, disc_courses in disciplines.items():
            valid_courses = [c for c in disc_courses if c['code'] != 'NEW' and c['code'].strip()]
            self.stdout.write(f"  {discipline}: {len(valid_courses)} courses")
        
        self.stdout.write("\nOverall Statistics:")
        self.stdout.write(f"  Created: {created_count}")
        self.stdout.write(f"  Updated: {updated_count}")
        self.stdout.write(f"  Skipped: {skipped_count}")
        self.stdout.write(f"  Total in database: {Course.objects.count()}")
        
        # Show some sample courses
        self.stdout.write(f"\nSample of imported courses:")
        self.stdout.write("-" * 40)
        sample_courses = Course.objects.all()[:5]
        for course in sample_courses:
            self.stdout.write(f"  {course.code}: {course.name} ({course.credits} credits)")

        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Course import completed successfully!")
        )