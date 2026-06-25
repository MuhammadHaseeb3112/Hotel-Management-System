# 🏨 Hotel Booking System

A modern Hotel Booking Management System built with **Django** that allows users to search hotels, book rooms, submit reviews, and manage reservations through an intuitive web interface. The project also includes an administrative dashboard for managing hotels, bookings, and customer inquiries.

---

## 📌 Features

### 👤 User Features

* User Registration & Login
* Secure Authentication
* Browse Hotels
* Search Hotels by Name or City
* Hotel Details with Multiple Images
* Room Availability Checking
* Online Booking System
* Booking Confirmation
* User Dashboard
* Hotel Reviews & Ratings
* Contact Form
* Responsive UI

---

### 🛠 Admin Features

* Admin Dashboard
* Manage Hotels
* Add New Hotels
* Edit Hotel Information
* Delete Hotels
* Upload Multiple Hotel Images
* Manage Bookings
* Approve Pending Bookings
* View Customer Contact Messages
* View Booking Statistics

---

## 🚀 Tech Stack

### Backend

* Python 3
* Django 5.x

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap

### Database

* SQLite3

### Other Technologies

* Django ORM
* JSONField
* Django Authentication
* Gmail SMTP Email Integration

---

# Project Structure

```
hotel_booking/
│
├── booking_app/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── hotel_booking/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── media/
├── static/
├── templates/
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---

# Database Models

## Hotel

Stores hotel information including:

* Hotel Name
* City
* Address
* Price Per Night
* Number of Rooms
* Multiple Images
* Amenities
* Featured Hotel

---

## Booking

Stores booking details:

* Customer Name
* Email
* Phone Number
* Hotel
* Check-in Date
* Check-out Date
* Number of Rooms
* Total Price
* Booking Status
* Booking Date

---

## Feedback

Allows authenticated users to submit:

* Hotel Rating
* Review
* Comment

---

## Contact Message

Stores messages submitted through the Contact page.

---

# Authentication

* User Registration
* Login
* Logout
* Protected User Dashboard
* Admin-only Dashboard

---

# Booking Workflow

1. User searches for hotels.
2. User selects a hotel.
3. User enters booking details.
4. System checks room availability.
5. Booking is stored in the database.
6. Admin reviews and approves bookings.
7. User can view bookings from the dashboard.

---

# Room Availability

The system automatically checks:

* Existing bookings
* Overlapping reservation dates
* Remaining available rooms

This prevents overbooking.

---

# Admin Dashboard

The admin panel allows administrators to:

* View total hotels
* View total bookings
* View pending bookings
* Manage hotels
* Upload hotel images
* Edit hotel information
* Delete hotels
* Manage customer bookings
* View contact messages

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/hotel-booking-system.git
```

Navigate into the project

```bash
cd hotel-booking-system
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Create a superuser

```bash
python manage.py createsuperuser
```

Run the development server

```bash
python manage.py runserver
```

Open your browser

```
http://127.0.0.1:8000/
```

---

# Email Configuration

Configure Gmail SMTP inside your `.env` or `settings.py`.

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
```

---

# Screenshots

Add screenshots of:

* Home Page
* Hotels Page
* Booking Page
* User Dashboard
* Admin Dashboard
* Contact Page

---

# Future Improvements

* Online Payment Gateway
* Stripe Integration
* JazzCash & EasyPaisa
* Hotel Categories
* Wishlist
* Booking Cancellation
* Email Notifications
* Booking History
* REST API
* Docker Deployment
* PostgreSQL Support

---

# Author

**Muhammad Haseeb**

Software Developer

GitHub:
https://github.com/MuhammadHaseeb3112

LinkedIn:
https://www.linkedin.com/

---

# License

This project is developed for educational and portfolio purposes.
