from django.db import models
from django.contrib.auth.models import AbstractUser

class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser, AuditModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.username

class Vehicle(AuditModel):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

    def delete(self, *args, **kwargs):
        if self.owner.is_staff:
            super().delete(*args, **kwargs)

class Owner(AuditModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    vehicles = models.ManyToManyField(Vehicle, related_name='owners')

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        if self.user.is_staff:
            super().delete(*args, **kwargs)

class Companion(AuditModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='companion_profile')

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        if self.user.is_staff:
            super().delete(*args, **kwargs)

class Contract(AuditModel):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts_as_driver')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateField()
    departure_time = models.TimeField()
    return_time = models.TimeField()
    seats_available = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    companions_limit = models.PositiveIntegerField()

    def __str__(self):
        return f"Contract by {self.driver.username} on {self.date}"

    def delete(self, *args, **kwargs):
        if self.driver.is_staff:
            super().delete(*args, **kwargs)
