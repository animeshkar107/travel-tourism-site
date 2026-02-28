from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('packages/', views.packages, name="packages"),
    path('book/<int:package_id>/', views.book_package, name="book"),
    path('register/', views.register, name='register'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('payment/<int:booking_id>/', views.payment_view, name='payment'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]

