from datetime import datetime
from flask import Blueprint, jsonify, request

from app.database import db
from app.models.meal import Meal
from app.models.food import Food
from app.models.meal_food import MealFood 
from app.models.plan_meal import PlanMeal 

from app.utils.nutrion_model import *

meal_bp = Blueprint("meal", __name__,url_prefix="/api/meal")

@meal_bp.route('/generate-plan', methods=['POST'])
def generate_plan():
    data = request.get_json()
    required_fields = ['id','objective','number-days']
    
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Todos los campos son requeridos."}), 400

    # Extraer parámetros
    client_id = data['id']
    objective = data['objective']
    numbers_days = data['number-days']
    
    return generate_plan_nutritional1(client_id,numbers_days,objective)

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

def save_meal(objective,type, calories, food, plan_id):
    """
    Create a new meal with the provided parameters.
    """
    proteins = float(calculate_proteins(food))
    fats = float(calculate_fats(food))
    carbohydrates = float(calculate_carbohydrates(food))
    print("proteins", proteins)
    print("fats", fats)
    print("carbohydrates", carbohydrates)
    meal = Meal(
        name=type,
        status=False,
        meal_type=type,
        total_calories=float(calories),
        total_proteins=proteins,
        total_fats=fats,
        total_carbohydrates=carbohydrates,
    )


    db.session.add(meal)
    db.session.commit()

    save_food(food, meal)

    return meal

def save_food(food, meal):
    for foo in food:
        foo['cantidad'] = float(foo['cantidad'])  # Conversión aquí

        f = Food.query.filter_by(name=foo['alimento']).first()
        meal_food = MealFood(meal_id=meal.id,
                            food_id=f.id,
                            quantity=foo['cantidad'], 
                            type_quantity=foo['unidad'])
        db.session.add(meal_food)    
    db.session.commit()

def save_plan_meal(meal, plan_id, date,day):
    """
    Crea un plan de comida con el id del plan y el id de la comida.
    """
    plan_meal = PlanMeal( plan_id=plan_id, meal_id=meal.id,date=date,day=day)
    db.session.add(plan_meal)
    db.session.commit()

    return plan_meal

def get_calories_plan(plan_id):
    meals = PlanMeal.query.filter_by(plan_id=plan_id).all()
    total_calories = 0
    for meal in meals:
        me = Meal.query.filter_by(id=meal.meal_id).first()
        total_calories += me.total_calories 
    return total_calories       

def calculate_proteins(food):
    print("comida recibida:", food)
    pro = 0
    for foo in food:
        if 'alimento' not in foo:
            print("Key 'alimento' no se encuentra en el item:", foo)
            continue
        pro_food = Food.query.filter_by(name=foo['alimento']).first()
        if pro_food:
            pro += pro_food.proteins
        else:
            print(f"Food '{foo['alimento']}' no encontrado en la base de datos.")
    return pro

def calculate_fats(food):
    print("comida recibida:", food)
    fats = 0
    for foo in food:
        if 'alimento' not in foo:
            print("Key 'alimento' no se encuentra en el item:", foo)
            continue
        fats_food = Food.query.filter_by(name=foo['alimento']).first()
        if fats_food:
            fats += fats_food.fats
        else:
            print(f"Food '{foo['alimento']}' no encontrado en la base de datos.")
    return fats

def calculate_carbohydrates(food):
    print("comida recibida:", food)
    carbohydrates = 0
    for foo in food:
        if 'alimento' not in foo:
            print("Key 'alimento' no se encuentra en el item:", foo)
            continue
        carbohydrates_food = Food.query.filter_by(name=foo['alimento']).first()
        if carbohydrates_food:
            carbohydrates += carbohydrates_food.carbohydrates
        else:
            print(f"Food '{foo['alimento']}' no encontrado en la base de datos.")
    return carbohydrates

