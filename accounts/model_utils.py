import requests

API_KEY = "62c82155ebda44cbaeed4927ea08fdc9"

def get_recipes_from_spoonacular(ingredients, user_utensils, recipe_count=5, cuisine=None):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "apiKey": API_KEY,
        "ingredients": ",".join(ingredients),
        "number": recipe_count,
        "ranking": 1,
    }

    # Add cuisine to the parameters only if provided
    if cuisine:
        params["cuisine"] = cuisine

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return {"error": response.text}

        recipes = response.json()

        # Additional details like utensils and equipment
        for recipe in recipes:
            recipe_id = recipe.get("id")
            info_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
            info_params = {"apiKey": API_KEY}

            info_response = requests.get(info_url, params=info_params)
            if info_response.status_code == 200:
                recipe_info = info_response.json()
                equipment = [item["name"] for item in recipe_info.get("equipment", [])]

                recipe["utensils"] = {
                    "all": equipment,
                    "used": [utensil for utensil in user_utensils if utensil in equipment],
                    "missing": [utensil for utensil in equipment if utensil not in user_utensils],
                }

        return recipes
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
