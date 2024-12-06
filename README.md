# RAMU - Real-time Assistant for Meal Upkeep

RAMU is a Django-based web application designed to assist students in planning meals, managing pantry and utensils, generating recipes, and scheduling meals/groceries. The application integrates with the Spoonacular API to provide recipe suggestions and supports calendar integration for event scheduling.

## Features
- **Pantry Management**: Add, view, and delete pantry items.
- **Utensil Management**: Manage your utensils inventory.
- **Recipe Suggestions**: Generate recipes based on available pantry items, cuisine preferences, intolerances and cooking time.
- **Calendar Integration**: Schedule meals and grocery shopping events with detailed notes.
- **User Authentication**: Secure login and registration features.
- **API Integration**: Utilizes the Spoonacular API for recipe generation.

---

## File Structure
Below is an overview of the important files and their purposes:

### Project-Level Files
- **`manage.py`**: Django's command-line utility for administrative tasks.
- **`ramu/settings.py`**: Configuration for the Django project (database, static files, installed apps, etc.).
- **`ramu/urls.py`**: URL routing configuration for the project.

### Application-Level Files (`accounts` app)
- **`views.py`**: Contains all the views handling user requests (e.g., adding pantry items, managing events).
- **`models.py`**: Defines the database models for pantry items, utensil items, and calendar events.
- **`urls.py`**: URL routing for the `accounts` app.
- **`templates/accounts/`**: HTML templates for rendering various pages (e.g., `welcome.html`, `main_welcome.html`).

### API Integration
- **Spoonacular API**: Used for recipe generation based on pantry ingredients, cooking time, and dietary preferences. API calls are made from `generate_recipe` in `views.py`.

---

## Requirements
To run this project, ensure you have the following installed:
- Python 3.8 or higher
- PostgreSQL database
- Django 5.1 or higher
- Requests library for API calls

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone git@github.com:shivalikac/ramu.git
   cd ramu

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  
   # On Windows: venv\Scripts\activate

3. **Configure the Database**

   You need to install PostgreSQL if not already installed.
   Create a database and user in PostgreSQL and update DATABASES in ramu/settings.py:

   ```CREATE DATABASE ramustore;
   CREATE USER ramu WITH PASSWORD 'kaka';
   GRANT ALL PRIVILEGES ON DATABASE ramustore TO ramu;

   DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'ramustore',
         'USER': 'ramu',
         'PASSWORD': 'kaka',
         'HOST': 'localhost',
         'PORT': '5432',
      }
   }

4. **Apply Migrations**

   Initialize the database by running:
   ``` bash
   python manage.py migrate

5. **Create a Superuser**
   ```bash
   python manage.py createsuperuser

6. **Run the Server**
   ``` bash
   python manage.py runserver


Now you can access the application at http://127.0.0.1:8000/main


## User Guide
This guide will provide an overview of how to navigate and use the RAMU application effectively.

1. Go on the URL http://127.0.0.1:8000/ to access the main page
2. Log in with your registered credentials or create a new account.
3. Navigate to the Your Pantry section on the main dashboard.
   - **Add Pantry Items**: 
      - Enter the item name and quantity in the respective fields.
      - Click the Add button or press Enter.
   - All added pantry items will appear in a list.
   - Click the Delete button next to any item to remove it.
4. Navigate to the Your Utensils section.
   - Add Utensils:
      - Enter the utensil name and quantity.
      - Click the Add button or press Enter.
   - All added utensils will be displayed in a list.
   - Click the Delete button next to any utensil to remove it.
5. Generate Recipes
   - Navigate to the Filters for Recipes section.
   - Apply Filters:
      - Maximum cooking time (e.g., 30 minutes).
      - Number of recipes to generate (e.g., 5).
      - Preferred cuisine type (e.g., Indian, Italian).
      - Intolerances or allergies (e.g., gluten, dairy).
   - Click the Generate Recipe button.
   - Recipe suggestions based on your pantry items will appear below.
   - Each recipe includes Title, Image, Used and missing ingredients and Link to the full recipe
   - It also includes an option to Add to Calendar:
      - Click Add to Calendar next to a recipe.
      - Select a date and meal type (Lunch/Dinner).
      - Save the event to schedule it in the calendar.
6. Calendar Integration
   - Navigate to the Meal Planning Calendar page under the schedule drop down.
   - See scheduled meals and grocery shopping events on the calendar.
   - Click Add Meal Manually or Add Grocery Shopping.
   - Click on any scheduled event to view or edit notes for future reference.
   - Click the Delete button next to an event to remove it.
7. Profile Management
   - Navigate to the Profile page (via the navigation bar).
   - See your account details.
