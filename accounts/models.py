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

class CalendarEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)
    #recipe_id = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField()
    meal_type = models.CharField(
        max_length=10,
        choices=[('lunch', 'Lunch'), ('dinner', 'Dinner')],
        default='lunch'  # Set default to "Lunch"
    )

    recipe_id = models.IntegerField(blank=True, null=True)  # Recipe ID from Spoonacular
    recipe_url = models.URLField(blank=True, null=True)  # Link to the Spoonacular recipe
    notes = models.TextField(blank=True, null=True)  # Notes for the recipe

    def __str__(self):
        return f"{self.title} on {self.date} ({self.meal_type}) for {self.user.username}"
