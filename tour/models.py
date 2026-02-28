from django.db import models
from django.contrib.auth.models import User


class Destination(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    # image = models.ImageField(upload_to='destinations/')
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Package(models.Model):
    title = models.CharField(max_length=200)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    price = models.IntegerField()
    duration = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    persons = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default="Pending")
    booking_date = models.DateTimeField(auto_now_add=True)  # ✅ automatically sets time

    def __str__(self):
        return f"{self.user.username} - {self.package.title}"

