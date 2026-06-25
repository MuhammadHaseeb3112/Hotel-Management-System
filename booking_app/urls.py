from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # frontend
    path('', views.home, name='home'),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),

    path('get-hotels/', views.get_hotels, name='get_hotels'),
    path('success/', views.success, name='success'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('support/', views.support, name='support'),
    path('hotels/', views.hotels, name='hotels'),
    path('hotels/<str:city>/', views.hotels_by_city, name='hotels_by_city'),
    path("submit-feedback/<int:hotel_id>/", views.submit_feedback, name="submit_feedback"),
    path("save-booking/", views.save_booking, name="save_booking"),

    # dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/hotels/', views.manage_hotels, name='manage_hotels'),
    path('dashboard/hotel/add/', views.add_hotel, name='add_hotel'),
    path('dashboard/hotel/delete/<int:id>/', views.delete_hotel, name='delete_hotel'),
    path('dashboard/bookings/', views.manage_bookings, name='manage_bookings'),
    path('dashboard/booking/update/<int:id>/', views.update_booking_status, name='update_booking'),
    path('dashboard/hotel/edit/<int:id>/', views.edit_hotel, name='edit_hotel'),
    path("user/dashboard/", views.user_dashboard, name="user_dashboard"),
    path('dashboard/contact-messages/', views.contact_messages, name='contact_messages'),
]
    
    



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)