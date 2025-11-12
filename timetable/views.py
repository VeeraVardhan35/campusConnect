# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from .models import Classroom, ClassSchedule, TimeSlot, Batch
from users.models import EmailGroup
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, time, date, timedelta
from .models import Classroom, ClassroomBooking, ClassSchedule, TimeSlot, Batch
from .forms import ClassroomBookingForm
from django.http import JsonResponse
from django.db.models import Q

@login_required
def weekly_timetable(request):
    """Show weekly timetable - simplified version without custom filters"""
    user = request.user
    
    # Get classes based on user role
    if user.role == 'student':
        try:
            student_profile = user.student_profile
            # Find batches that match the student's batch and branch
            student_batches = Batch.objects.filter(
                batch_year=student_profile.batch,
                branch=student_profile.branch
            )
            classes = ClassSchedule.objects.filter(batch__in=student_batches).select_related(
                'course', 'professor', 'classroom', 'time_slot', 'batch'
            )
        except Exception as e:
            classes = ClassSchedule.objects.none()
    elif user.role == 'professor':
        classes = ClassSchedule.objects.filter(professor=user).select_related(
            'course', 'professor', 'classroom', 'time_slot', 'batch'
        )
    else:
        classes = ClassSchedule.objects.all().select_related(
            'course', 'professor', 'classroom', 'time_slot', 'batch'
        )
    
    # Get all days and time slots
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    time_slots = TimeSlot.objects.all().order_by('start_time')
    
    context = {
        'classes': classes,
        'days': days,
        'time_slots': time_slots,
    }
    return render(request, 'timetable/weekly_timetable.html', context)

@login_required
def classroom_status(request):
    """Show classroom status with enhanced current class information"""
    now = timezone.now()
    current_time = now.time()
    current_day = now.strftime('%A').lower()
    
    classrooms = Classroom.objects.all().order_by('building', 'room_number')
    classroom_data = []
    
    for classroom in classrooms:
        status = 'free'
        current_class = None
        next_class = None
        
        # Check for ongoing classes
        ongoing_classes = ClassSchedule.objects.filter(
            classroom=classroom,
            time_slot__day=current_day,
            time_slot__start_time__lte=current_time,
            time_slot__end_time__gte=current_time
        ).select_related('course', 'professor', 'time_slot', 'batch')
        
        if ongoing_classes.exists():
            current_class = ongoing_classes.first()
            status = 'ongoing'
        else:
            # Check for upcoming classes today
            upcoming_classes = ClassSchedule.objects.filter(
                classroom=classroom,
                time_slot__day=current_day,
                time_slot__start_time__gt=current_time
            ).select_related('course', 'professor', 'time_slot', 'batch').order_by('time_slot__start_time')
            
            if upcoming_classes.exists():
                current_class = upcoming_classes.first()
                status = 'scheduled'
                # Get the next class after the current scheduled one
                if upcoming_classes.count() > 1:
                    next_class = upcoming_classes[1]
            else:
                # Check if there were classes today
                past_classes = ClassSchedule.objects.filter(
                    classroom=classroom,
                    time_slot__day=current_day,
                    time_slot__end_time__lt=current_time
                )
                
                if past_classes.exists():
                    status = 'completed'
        
        classroom_data.append({
            'classroom': classroom,
            'status': status,
            'current_class': current_class,
            'next_class': next_class,
        })
    
    # Get email groups
    batch_groups = EmailGroup.objects.filter(group_type='batch', is_active=True).order_by('batch')
    branch_groups = EmailGroup.objects.filter(group_type='branch', is_active=True).order_by('batch', 'branch')
    
    # Organize branch groups by batch for better display
    branch_groups_by_batch = {}
    for group in branch_groups:
        if group.batch not in branch_groups_by_batch:
            branch_groups_by_batch[group.batch] = []
        branch_groups_by_batch[group.batch].append(group)
    
    context = {
        'classroom_data': classroom_data,
        'current_time': now,
        'batch_groups': batch_groups,
        'branch_groups_by_batch': branch_groups_by_batch,
    }
    return render(request, 'timetable/classroom_status.html', context)


@login_required
def professor_dashboard(request):
    if request.user.role != 'professor':
        messages.error(request, "Access denied. Professor access required.")
        return redirect('home')
    
    # Get professor's upcoming classes
    upcoming_classes = ClassSchedule.objects.filter(
        professor=request.user,
        time_slot__day=timezone.now().strftime('%A').lower()
    ).select_related('course', 'classroom', 'time_slot', 'batch').order_by('time_slot__start_time')
    
    # Get professor's bookings
    bookings = ClassroomBooking.objects.filter(professor=request.user).order_by('-date', '-start_time')[:5]
    
    context = {
        'upcoming_classes': upcoming_classes,
        'bookings': bookings,
        'current_time': timezone.now(),
    }
    return render(request, 'timetable/professor_dashboard.html', context)

@login_required
def free_slots(request):
    """Show classrooms and their availability based on schedule + bookings."""
    if not hasattr(request.user, "role") or request.user.role != "professor":
        messages.error(request, "Access denied. Professors only.")
        return redirect("home")

    # Parse selected date
    selected_date_str = request.GET.get("date")
    if selected_date_str:
        try:
            selected_date = date.fromisoformat(selected_date_str)
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()

    day_name = selected_date.strftime("%A").lower()

    classrooms = Classroom.objects.all().order_by("building", "room_number")
    time_slots = [time(h, 0) for h in range(8, 20)]  # 08:00–19:00 every hour

    # Fetch schedules and bookings for that day
    schedules = ClassSchedule.objects.filter(
        time_slot__day=day_name
    ).select_related("classroom", "time_slot")

    bookings = ClassroomBooking.objects.filter(
        date=selected_date, status__in=["approved", "pending"]
    ).select_related("classroom")

    # Compute availability
    availability = {}

    for room in classrooms:
        availability[room.id] = {}
        for slot in time_slots:
            available = True

            # Check scheduled classes
            for s in schedules:
                if s.classroom_id == room.id:
                    if s.time_slot.start_time <= slot < s.time_slot.end_time:
                        available = False
                        break

            # Check existing bookings
            if available:
                for b in bookings:
                    if b.classroom_id == room.id:
                        if b.start_time <= slot < b.end_time:
                            available = False
                            break

            availability[room.id][slot.strftime("%H:%M")] = available

    context = {
        "classrooms": classrooms,
        "time_slots": time_slots,
        "availability": availability,
        "selected_date": selected_date,
        "prev_date": selected_date - timedelta(days=1),
        "next_date": selected_date + timedelta(days=1),
    }
    return render(request, "timetable/free_slots.html", context)



@login_required
def book_classroom(request, classroom_id, date_str, time_str):
    if request.user.role != 'professor':
        messages.error(request, "Access denied. Professor access required.")
        return redirect('home')
    
    classroom = get_object_or_404(Classroom, id=classroom_id)
    
    try:
        selected_date = date.fromisoformat(date_str)
        start_time = datetime.strptime(time_str, '%H:%M').time()
        # Default to 1 hour booking
        end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=1)).time()
    except (ValueError, TypeError):
        messages.error(request, "Invalid date or time format.")
        return redirect('free_slots')
    
    if request.method == 'POST':
        form = ClassroomBookingForm(request.POST, professor=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.professor = request.user
            booking.save()
            messages.success(request, f"Classroom booking request submitted for {classroom.room_number}!")
            return redirect('professor_dashboard')
    else:
        initial_data = {
            'classroom': classroom,
            'date': selected_date,
            'start_time': start_time,
            'end_time': end_time,
        }
        form = ClassroomBookingForm(initial=initial_data, professor=request.user)
    
    context = {
        'form': form,
        'classroom': classroom,
        'selected_date': selected_date,
        'start_time': start_time,
        'end_time': end_time,
    }
    return render(request, 'timetable/book_classroom.html', context)

@login_required
def my_bookings(request):
    if request.user.role != 'professor':
        messages.error(request, "Access denied. Professor access required.")
        return redirect('home')
    
    bookings = ClassroomBooking.objects.filter(professor=request.user).order_by('-date', '-start_time')
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'timetable/my_bookings.html', context)

@login_required
def cancel_booking(request, booking_id):
    if request.user.role != 'professor':
        messages.error(request, "Access denied. Professor access required.")
        return redirect('home')
    
    booking = get_object_or_404(ClassroomBooking, id=booking_id, professor=request.user)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
        return redirect('my_bookings')
    
    context = {
        'booking': booking,
    }
    return render(request, 'timetable/cancel_booking.html', context)