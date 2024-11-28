from datetime import datetime
from flask import Blueprint, jsonify, request

from app.database import db
from app.models.meal import Meal
from app.models.food import Food
from app.models.meal_food import MealFood  # Assuming you have this model for Meal-Food relationships

meal_bp = Blueprint("meal", __name__,url_defaults="api/meal")

@meal_bp.route('/meals/', methods=['GET'] )
def get_meal_by_objective():
    """
    Retrieves one breakfast, one lunch, and one dinner with their associated foods.
    """
    try:
        # Query the database for one breakfast, one lunch, and one dinner
        breakfasts = (
            Meal.query.filter_by(meal_type="desayuno", status=True)
            .first()
        )
        lunches = (
            Meal.query.filter_by(meal_type="almuerzo", status=True)
            .first()
        )
        dinners = (
            Meal.query.filter_by(meal_type="cena", status=True)
            .first()
        )
        
        # Format meals and their related foods into JSON format
        meals = {
            "breakfast": format_meal_with_foods(breakfasts) if breakfasts else None,
            "lunch": format_meal_with_foods(lunches) if lunches else None,
            "dinner": format_meal_with_foods(dinners) if dinners else None,
        }
        return jsonify(meals), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Unable to fetch meals"}), 500


def format_meal_with_foods(meal):
    """
    Helper function to format a meal with its associated foods.
    """
    if not meal:
        return None

    # Fetch associated foods through the MealFood relationship
    foods = (
        MealFood.query.filter_by(meal_id=meal.id)
        .join(Food, MealFood.food_id == Food.id)
        .all()
    )

    return {
        "id": meal.id,
        "name": meal.name,
        "meal_type": meal.meal_type,
        "total_calories": meal.total_calories,
        "total_proteins": meal.total_proteins,
        "total_fats": meal.total_fats,
        "total_carbohydrates": meal.total_carbohydrates,
        "foods": [
            {
                "name": food.food.name,
                "quantity": food.quantity,
                "type_quantity": food.type_quantity,
                "calories": food.food.calories,
                "proteins": food.food.proteins,
                "fats": food.food.fats,
                "carbohydrates": food.food.carbohydrates,
            }
            for food in foods
        ],
    }