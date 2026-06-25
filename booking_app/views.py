from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ContactMessage, Hotel, Feedback, Booking
from .forms import BookingForm  
from django.views.decorators.csrf import csrf_exempt
import json
import re
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
import os
from datetime import datetime
from decimal import Decimal
from django.conf import settings
# views.py

from django.shortcuts import render
from .models import ContactMessage


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")  # Error message
    return render(request, "login.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")  # Error message
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect("home")
    return render(request, "signup.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def hotels_by_city(request, city):
    # Replace this with your actual hotel filtering logic
    hotels = [
        {"name": "Hotel Crown Lahore", "city": "Lahore", "address": "276, Block R2, Lahore"},
        {"name": "Grand Pakeeza Hotel", "city": "Lahore", "address": "R2 Block Road 57, Lahore"},
        {"name": "Best Western Premier", "city": "Islamabad", "address": "110 MM Alam Road, Islamabad"},
    ]
    filtered_hotels = [hotel for hotel in hotels if hotel["city"].lower() == city.lower()]
    return render(request, 'hotel.html', {'city': city, 'hotels': filtered_hotels})



def success(request):
    return render(request, "success.html")


# Create your views here.




def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Save the message to the database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")  # Redirect to the contact page after submission

    return render(request, 'contact.html')



def about(request):
    return render(request, 'about.html')

def home(request):
    query = request.GET.get('query', '').strip().lower()
    city = request.GET.get('city', '').strip().lower()

    if query:
        hotels = Hotel.objects.filter(name__icontains=query, default=False)
    elif city:
        hotels = Hotel.objects.filter(city__iexact=city, default=False)
    else:
        hotels = Hotel.objects.filter(default=True)

    return render(request, 'home.html', {'hotels': hotels})
 # Ensure 'home.html' extends 'base.html'

def support(request):
    return render(request, 'support.html')

def hotels(request):
    return render(request, 'hotel.html')

# changes made on 28/03/2025



@login_required
def submit_feedback(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")

        # Ensure the user has stayed at the hotel (logic depends on your booking system)
        # For example, check if the user has a completed booking for this hotel
        # if not user_has_stayed_at_hotel(request.user, hotel):
        #     return JsonResponse({"error": "You can only leave feedback for hotels you have stayed in."}, status=403)

        Feedback.objects.create(
            hotel=hotel,
            user=request.user,
            rating=rating,
            comment=comment,
        )
        return JsonResponse({"success": "Feedback submitted successfully."})

    return JsonResponse({"error": "Invalid request method."}, status=400)

def get_hotels(request):
    query = request.GET.get('query', '').strip().lower()
    city = request.GET.get('city', '').strip().lower()

    try:
        # Filter hotels based on query and city
        if city == "all":  # Show all hotels
            hotels = Hotel.objects.all()
        elif city:  # Filter by city
            hotels = Hotel.objects.filter(city__icontains=city)
        elif query:  # Search by hotel name
            hotels = Hotel.objects.filter(name__icontains=query)
        else:  # Default behavior: show only default hotels
            hotels = Hotel.objects.all()   # ✅ FIXED


        hotels_data = []
        for hotel in hotels:
            # Use the `images` field directly (it's a JSONField storing a list of image paths)
            images = hotel.images if hotel.images else ["/static/images/placeholder.jpg"]  # Fallback placeholder image

            # Add hotel data
            hotels_data.append({
                "id": hotel.id,
                "name": hotel.name,
                "city": hotel.city,
                "price_per_night": hotel.price_per_night,
                "address": hotel.address,
                "images": images,
                "amenities": hotel.amenities,  # Directly use the `amenities` JSONField
            })

        return JsonResponse({"hotels": hotels_data})
    except Exception as e:
        # Log the error and return a 500 response
        print(f"Error in get_hotels view: {e}")
        return JsonResponse({"error": "An error occurred while fetching hotels."}, status=500)
    




@csrf_exempt
def save_booking(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)

            # Extract fields
            customer_name = data.get("customer_name")
            email = data.get("email")
            phone_number = data.get("phone_number")
            check_in_date = data.get("check_in_date")
            check_out_date = data.get("check_out_date")
            number_of_rooms = int(data.get("number_of_rooms") or 1)
            total_price = data.get("total_price")
            hotel_id = data.get("hotel_id")
            card_number = data.get("card_number")

            # Validate required fields
            if not all([customer_name, email, phone_number, check_in_date, check_out_date, hotel_id, card_number]):
                return JsonResponse({"error": "Missing required fields."}, status=400)

            # 🔥 FIX 1: Convert dates (CRITICAL)
            check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d").date()

            # 🔥 FIX 2: Convert price safely
            total_price = Decimal(total_price)

            # Validate card
            if not validate_card_number(card_number):
                return JsonResponse({"error": "Invalid card number."}, status=400)

            # Get hotel
            try:
                hotel = Hotel.objects.get(id=hotel_id)
            except Hotel.DoesNotExist:
                return JsonResponse({"error": "Hotel not found."}, status=404)

            # 🔥 FIX 3: Availability check (now correct)
            is_available, available_rooms = check_room_availability(
                hotel,
                check_in_date,
                check_out_date,
                number_of_rooms
            )

            if not is_available:
                return JsonResponse({
                    "error": f"Only {available_rooms} rooms available"
                }, status=400)

            # Save booking
            booking = Booking.objects.create(
                user=request.user if request.user.is_authenticated else None,
                customer_name=customer_name,
                email=email,
                phone_number=phone_number,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                number_of_rooms=number_of_rooms,
                total_price=total_price,
                hotel=hotel,
            )

            print("Booking saved:", booking)

            return JsonResponse({"success": "Booking confirmed!"})

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)
            


def validate_card_number(card_number):
    """
    Validate the card number for Visa and MasterCard.
    Visa: Starts with 4, 16 digits.
    MasterCard: Starts with 51-55 or 2221-2720, 16 digits.
    """
    visa_pattern = r"^4\d{15}$"
    mastercard_pattern = r"^(5[1-5]\d{14}|2(2[2-9]\d{12}|[3-6]\d{13}|7[01]\d{12}|720\d{12}))$"

    if re.match(visa_pattern, card_number) or re.match(mastercard_pattern, card_number):
        return True
    return False



def check_room_availability(hotel, check_in_date, check_out_date, requested_rooms):
    # Get overlapping bookings
    overlapping_bookings = Booking.objects.filter(
        hotel=hotel,
        check_in_date__lt=check_out_date,
        check_out_date__gt=check_in_date
    )

    # Total already booked
    rooms_booked = sum(b.number_of_rooms for b in overlapping_bookings)

    # Prevent negative values
    available_rooms = max(0, hotel.number_of_rooms - rooms_booked)

    print("DEBUG → Total:", hotel.number_of_rooms,
          "Booked:", rooms_booked,
          "Available:", available_rooms)

    return available_rooms >= requested_rooms, available_rooms





# ================= DASHBOARD =================

@staff_member_required
def admin_dashboard(request):
    return render(request, "dashboard/index.html", {
        "total_hotels": Hotel.objects.count(),
        "total_bookings": Booking.objects.count(),
        "pending": Booking.objects.filter(status="pending").count(),
    })


# ================= HOTELS =================

@staff_member_required
def manage_hotels(request):
    hotels = Hotel.objects.all().order_by("-id")
    return render(request, "dashboard/hotels.html", {"hotels": hotels})


# ================= ADD HOTEL =================
@staff_member_required
def add_hotel(request):
    if request.method == "POST":

        hotel = Hotel.objects.create(
            name=request.POST.get("name"),
            city=request.POST.get("city"),
            price_per_night=request.POST.get("price"),
            address=request.POST.get("address"),
            number_of_rooms=request.POST.get("rooms"),
            default=True if request.POST.get("default") == "on" else False,
            amenities=[
                a.strip() for a in request.POST.get("amenities", "").split(",") if a.strip()
            ]
        )

        # 🔥 MULTIPLE IMAGE UPLOAD (SAFE + UNIQUE)
        image_urls = []

        for file in request.FILES.getlist("images"):
            import uuid

            file_name = f"{uuid.uuid4()}_{file.name}"
            file_path = f"hotels/{file_name}"

            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            image_urls.append(settings.MEDIA_URL + file_path)

        hotel.images = image_urls
        hotel.save()

        return redirect("manage_hotels")

    return render(request, "dashboard/add_hotel.html")

# ================= EDIT HOTEL =================

@staff_member_required
def edit_hotel(request, id):
    hotel = get_object_or_404(Hotel, id=id)

    if request.method == "POST":

        hotel.name = request.POST.get("name")
        hotel.city = request.POST.get("city")
        hotel.price_per_night = request.POST.get("price")
        hotel.address = request.POST.get("address")
        hotel.number_of_rooms = request.POST.get("rooms")

        hotel.default = True if request.POST.get("default") == "on" else False

        hotel.amenities = [
            a.strip() for a in request.POST.get("amenities", "").split(",") if a.strip()
        ]

        # ✅ SAFE COPY
        updated_images = hotel.images.copy() if hotel.images else []

        # 🔥 DELETE SELECTED IMAGES
        delete_images = request.POST.getlist("delete_images")

        for img in delete_images:
            if img in updated_images:
                updated_images.remove(img)

        # 🔥 ADD NEW IMAGES
        for file in request.FILES.getlist("images"):
            file_path = f"hotels/{file.name}"

            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "wb+") as f:
                for chunk in file.chunks():
                    f.write(chunk)

            updated_images.append(settings.MEDIA_URL + file_path)

        hotel.images = updated_images
        hotel.save()

        return redirect("manage_hotels")

    return render(request, "dashboard/edit_hotel.html", {"hotel": hotel})

# ================= DELETE HOTEL =================

@staff_member_required
def delete_hotel(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    hotel.delete()
    return redirect("manage_hotels")


# ================= BOOKINGS =================

@staff_member_required
def manage_bookings(request):
    bookings = Booking.objects.all().order_by("-booking_date")
    return render(request, "dashboard/bookings.html", {"bookings": bookings})


# ================= UPDATE BOOKING =================


@staff_member_required
def update_booking_status(request, id):
    booking = get_object_or_404(Booking, id=id)

    if request.method == "POST":
        status = request.POST.get("status")

        if status in ["pending", "approved", "rejected"]:
            booking.status = status
            booking.save()

    return redirect("manage_bookings")


@login_required
def user_dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')

    return render(request, "user/dashboard.html", {
        "bookings": bookings
    })



from django.shortcuts import render
from .models import ContactMessage

def contact_messages(request):

    messages = ContactMessage.objects.all().order_by('-created_at')

    return render(
        request,
        'dashboard/contact_messages.html',
        {'messages': messages}
    )