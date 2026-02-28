from django.shortcuts import render, redirect
from .models import Destination, Package, Booking
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login

from django.shortcuts import get_object_or_404
from .models import Package, Booking

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def home(request):
    destinations = Destination.objects.all()
    return render(request, "tour/home.html", {"destinations": destinations})


def packages(request):
    packages = Package.objects.all()
    return render(request, "tour/packages.html", {"packages": packages})


@login_required
def book_package(request, package_id):
    package = Package.objects.get(id=package_id)

    if request.method == "POST":
        persons = request.POST['persons']
        Booking.objects.create(
            user=request.user,
            package=package,
            persons=persons
        )
        return redirect("my_bookings")

    return render(request, "tour/book.html", {"package": package})



def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST['confirm_password']

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter a valid email address!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        user = User.objects.create_user(
        username=username,
        email=email,
        password=password
        )
        login(request, user)
        return redirect('home')

    return render(request, "tour/register.html")

@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if request.method == "POST":
        # Simulate payment success
        booking.status = "Confirmed"
        booking.save()
        messages.success(request, "Payment successful! Booking confirmed.")
        return redirect('my_bookings')

    return render(request, 'tour/payment.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)

    for b in bookings:
        b.total_amount = b.package.price * b.persons

    return render(request, "tour/my_bookings.html", {"bookings": bookings})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if booking.status == "Pending":
        booking.status = "Cancelled"
        booking.save()
        messages.success(request, "Booking cancelled successfully!")
    else:
        messages.error(request, "Only pending bookings can be cancelled!")

    return redirect('my_bookings')