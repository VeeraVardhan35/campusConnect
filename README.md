<img src="https://res.cloudinary.com/db0qkzn6a/image/upload/v1767260974/gitdocs/user_37ePKxY5vSi8rwneg3BVgd3ZKXq/images/bnohsduwimpt317gmpcn.png"
     alt="CampusConnect Banner"
     style="width:100%; max-height:360px; object-fit:cover;" />

# CampusConnect 🎓

**Live Demo:** https://veeravardhan.pythonanywhere.com/

CampusConnect is a **Django-based campus management system** designed to handle **academic timetables, classroom scheduling, and professor booking workflows**.  
It supports **students, professors, and admins** with secure authentication, OTP-based email verification, and role-based dashboards.

---

## ✨ Features

### 🔐 Authentication & Users
- Custom Django `AUTH_USER_MODEL`
- Role-based users: **Student / Professor / Admin**
- OTP-based email verification
- Password reset via email
- Student & professor profile management

### 📅 Timetable Management
- Weekly timetable view for students (batch-wise)
- Weekly timetable view for professors
- Course, batch, classroom, and timeslot mapping
- Current and next class indicators

### 🏫 Classroom Booking System
- Classroom availability checking
- Professor-only booking requests
- View free slots by date
- My bookings & cancel booking flow
- Booking purpose and course association

### ⚙️ Developer Utilities
- Multiple Django **management commands** for:
  - Seeding sample data
  - Generating test users
  - Creating email groups
- Environment-based configuration using `python-dotenv`
- CI workflow for automated deployment

---

## 🧠 Tech Stack

**Backend**
- Python 3.10+
- Django 5.2.8

**Database**
- SQLite (default, easy local setup)
- Easily swappable with PostgreSQL/MySQL

**Frontend**
- Django Templates
- Bootstrap 5

**Other Tools**
- Pillow (image handling)
- python-dotenv
- GitHub Actions (CI)
- PythonAnywhere (deployment)

---

## 📸 Screenshots / Demo

<img src="https://res.cloudinary.com/db0qkzn6a/image/upload/v1767260978/gitdocs/user_37ePKxY5vSi8rwneg3BVgd3ZKXq/images/tmx8gblxvhjkvc8my6hj.png"
     alt="Weekly Timetable View"
     style="width:100%; max-width:1100px; display:block; margin:16px auto;" />

Try it live → https://veeravardhan.pythonanywhere.com/

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
- Python 3.10+
- Git
- Virtualenv (recommended)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/VeeraVardhan35/campusConnect.git
cd campusConnect
