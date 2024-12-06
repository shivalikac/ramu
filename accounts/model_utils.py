import requests

# Spoonacular API key
API_KEY = "62c82155ebda44cbaeed4927ea08fdc9"

def get_recipes_from_spoonacular(ingredients, user_utensils, recipe_count=5, cuisine=None, cooking_time=None):
    """
    Fetch recipes from the Spoonacular API based on ingredients and user preferences.

    Args:
        ingredients (list): List of ingredients available to the user.
        user_utensils (list): List of utensils available to the user.
        recipe_count (int): Number of recipes to fetch (default is 5).
        cuisine (str): Optional cuisine preference (e.g., 'Italian', 'Mexican').
        cooking_time (int): Optional maximum cooking time in minutes.

    Returns:
        list | dict: List of recipes with details or a dictionary containing an error message.
    """
    # Endpoint for finding recipes by ingredients
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "apiKey": API_KEY,
        "ingredients": ",".join(ingredients),  
        "number": recipe_count,  
        "ranking": 1,  # Prioritize recipes with more ingredients matches
    }

    # Add optional filters to the API request
    if cuisine:
        params["cuisine"] = cuisine  
    if cooking_time:
        params["maxReadyTime"] = cooking_time 

    try:
        # Make the initial request to fetch recipes
        response = requests.get(url, params=params)
        if response.status_code != 200:
            # Return error message if the API call fails
            return {"error": response.text}

        # Parse the JSON response
        recipes = response.json()

        # Fetch additional details like utensils and equipment for each recipe
        for recipe in recipes:
            recipe_id = recipe.get("id")  # Get the recipe ID
            info_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
            info_params = {"apiKey": API_KEY}

            # Make a request for detailed recipe information
            info_response = requests.get(info_url, params=info_params)
            if info_response.status_code == 200:
                recipe_info = info_response.json()
                equipment = [item["name"] for item in recipe_info.get("equipment", [])]

                # Add utensils comparison to the recipe details
                recipe["utensils"] = {
                    "all": equipment,
                    "used": [utensil for utensil in user_utensils if utensil in equipment], 
                    "missing": [utensil for utensil in equipment if utensil not in user_utensils], 
                }

        return recipes 

    except requests.exceptions.RequestException as e:
        # Handle exceptions during the API call
        return {"error": str(e)}
