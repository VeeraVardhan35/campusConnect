from django.urls import path
from . import views

urlpatterns = [
    path('classrooms/', views.classroom_status, name='classroom_status'),
    path('weekly/', views.weekly_timetable, name='weekly_timetable'),
    path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('professor/free-slots/', views.free_slots, name='free_slots'),
    path('professor/book/<int:classroom_id>/<str:date_str>/<str:time_str>/', views.book_classroom, name='book_classroom'),
    path('professor/my-bookings/', views.my_bookings, name='my_bookings'),
    path('professor/cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]