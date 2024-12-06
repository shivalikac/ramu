from django.db import models
from django.contrib.auth.models import User

class PantryItem(models.Model):
    """
    Represents an item in a user's pantry.

    Fields:
        user (ForeignKey): The user who owns this pantry item.
        item_name (CharField): The name of the pantry item.
        quantity (IntegerField): The quantity of the item (default is 1).
        date_added (DateTimeField): The date and time the item was added (auto-generated).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who owns this item
    item_name = models.CharField(max_length=255)  # Name of the pantry item
    quantity = models.IntegerField(default=1)  # Quantity of the item (default is 1)
    date_added = models.DateTimeField(auto_now_add=True)  # Automatically set when the item is created

    def __str__(self):
        return f"{self.item_name} (x{self.quantity}) for {self.user.username}"


class UtensilItem(models.Model):
    """
    Represents a utensil item in a user's inventory.

    Fields:
        user (ForeignKey): The user who owns this utensil item.
        utensil_name (CharField): The name of the utensil.
        quantity (IntegerField): The quantity of the utensil (default is 1).
        date_added (DateTimeField): The date and time the utensil was added (auto-generated).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who owns this utensil
    utensil_name = models.CharField(max_length=255)  # Name of the utensil
    quantity = models.IntegerField(default=1)  # Quantity of the utensil (default is 1)
    date_added = models.DateTimeField(auto_now_add=True)  # Automatically set when the item is created

    def __str__(self):
        return f"{self.utensil_name} (x{self.quantity}) for {self.user.username}"


class CalendarEvent(models.Model):
    """
    Represents an event on the user's calendar.

    Fields:
        user (ForeignKey): The user who owns this calendar event.
        title (CharField): The title of the event.
        image (URLField): Optional URL of an image associated with the event.
        date (DateField): The date of the event.
        meal_type (CharField): The type of meal (e.g., Lunch or Dinner) with choices.
        recipe_id (IntegerField): Optional ID of the associated recipe (from Spoonacular).
        recipe_url (URLField): Optional URL to the associated recipe.
        notes (TextField): Optional notes for the event or recipe.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who owns this event
    title = models.CharField(max_length=255)  # Title of the event
    image = models.URLField(blank=True, null=True)  # Optional URL of an image for the event
    date = models.DateField()  # Date of the event
    meal_type = models.CharField(
        max_length=10,
        choices=[('lunch', 'Lunch'), ('dinner', 'Dinner')],  # Predefined choices for meal type
        default='lunch',
        null=True,
        blank=True
    )
    recipe_id = models.IntegerField(blank=True, null=True)  # Optional recipe ID from Spoonacular
    recipe_url = models.URLField(blank=True, null=True)  # Optional URL to the associated recipe
    notes = models.TextField(blank=True, null=True)  # Optional notes for the event

    def __str__(self):
        """
        String representation of the CalendarEvent.

        Returns:
            str: A formatted string describing the event.
        """
        return f"{self.title} on {self.date} ({self.meal_type}) for {self.user.username}"
