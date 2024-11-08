from django.db import models
from django.contrib.auth.models import User

class PantryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

class UtensilItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    utensil_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
