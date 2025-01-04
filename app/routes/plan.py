from flask import Blueprint, jsonify, request
from datetime import datetime

from app.database import db
from app.models.meal import Meal
from app.models.food import Food
from app.models.plan import Plan
from app.models.plan_meal import PlanMeal
from app.models.health_profile import HealthProfile
from app.models.physical_activity import PhysicalActivity

from app.utils.functions import convertir_a_json
from app.utils.planner import Planner

from app.utils.nutrion_model import *
from app.routes.auth import token_required


plan_meal_bp = Blueprint("plan_meal", __name__, url_prefix="/api/plan-meal")

#con ia (token muy limitados)
@plan_meal_bp.route("/generate-plan", methods=["POST"])
@token_required
def generate_plan():
    data = request.get_json()
    required_fields = ["id", "objective", "number-days"]

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Todos los campos son requeridos."}), 400

    # Extraer parámetros
    client_id = data["id"]
    objective = data["objective"]
    numbers_days = data["number-days"]
    print("client_id", client_id)
    print("objective", objective)
    print("numbers_days", numbers_days)

    return generate_plan_nutritional(client_id, numbers_days, objective)

#con modelo de regresion
@plan_meal_bp.route("/generate-plan1", methods=["POST"])
@token_required
def generate_plan_1(current_user_id):
    """
    Generar un plan de comidas personalizado para un usuario específico. 
    Esta ruta recibe los datos del usuario y genera un plan de comidas basado 
    en sus necesidades calóricas, objetivos y número de días del plan. 
    La información generada incluye el perfil de salud,
    la actividad física y las comidas distribuidas. 
    ---
    tags:
      - Plan nutricional
    parameters:
      - name: Parámetros
        in: body
        required: true
        schema:
            type: object
            properties:
                id:
                    type: int
                    description: ID del cliente
                    example: 1
                objective:
                    type: string
                    description: El objetivo del plan (por ejemplo, "Perder peso")
                    example: "Perder peso"
                number-days:
                    type: int
                    description: El número de días para el plan.
                    example: 7
    responses:
        200:
            description: Plan de comidas generado con éxito
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Plan de comidas generado con éxito!"
                    plan:
                        type: object
                        description: Plan de comidas detallado generado
        500:
            description: Error al generar el plan de comidas
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Error al generar el plan de comidas"
    """
    data = request.get_json()
    client_id = current_user_id
    objective = data["objective"]
    numbers_days = data["number-days"]
    planner = Planner()

    healt_profile = HealthProfile.query.filter_by(user_id=client_id).first()
    pal = PhysicalActivity.query.filter_by(id=healt_profile.physical_activity_id).first()
    # Calcular las calorías necesarias para el plan completo
    calories_total = planner.calories(healt_profile.weight,
                                        healt_profile.height*100,
                                        healt_profile.age, 
                                        healt_profile.gender, 
                                        objective, pal.PAL, 
                                        numbers_days)
    
    plan= create_plan(objective, calories_total,client_id)

    # Ya se tiene DataFrame df_food con los alimentos disponibles
    plan_comidas = planner.distribuir_comidas( calories_total, numbers_days, objective, plan.id)
    #plan_comidas = planner.distribuir_comidas( calories_total, numbers_days, objective, 1)


    # Convertir el plan de comidas a JSON
    plan_json = convertir_a_json(plan_comidas)
    if plan_json is None:
        return jsonify({"message": "Error al generar el plan de comidas"}), 500
    return jsonify({
        "message": "Plan de comidas generado con éxito!",
        "plan": plan_json
    }), 200

def create_plan(objective, calories, user_id):
    # Crear un plan nutricional
    plan = Plan(name=objective,
                calories= calories,
                date_generation =datetime.now().strftime('%Y-%m-%d %H:%M:%S') ,
                status = "en progreso",
                user_id=user_id)
    db.session.add(plan)
    db.session.commit()
    return plan

#@plan_meal_bp.route("/get-plan/<int:user_id>", methods=["GET"])
@plan_meal_bp.route("/get-plan", methods=["GET"])
@token_required
def get_plan_by_user(current_user_id):
    """
    Obtener el plan de comidas actual para un usuario específico.
    Esta ruta devuelve el plan de comidas en progreso del usuario actual.
    Si no hay un plan activo, se devuelve un mensaje de error.
    ---
    tags:
      - Planes Nutricional
    parameters:
      - name: current_user_id
        in: path
        required: true
        description: ID del usuario actual obtenido del token.
        type: integer
        example: 1
    responses:
      200:
        description: Plan de comidas obtenido exitosamente.
        schema:
          type: object
          properties:
            plan_id:
              type: integer
              example: 1
            name:
              type: string
              example: "Plan semanal de pérdida de peso"
            calories:
              type: float
              example: 1800.0
            date_generation:
              type: string
              format: date-time
              example: "2025-01-01T10:00:00"
            status:
              type: string
              example: "En progreso"
            meals:
              type: array
              items:
                type: object
                properties:
                  meal_id:
                    type: integer
                    example: 2
                  name:
                    type: string
                    example: "Desayuno"
                  meal_type:
                    type: string
                    example: "Comida principal"
                  total_calories:
                    type: float
                    example: 400.0
                  total_proteins:
                    type: float
                    example: 25.0
                  total_fats:
                    type: float
                    example: 15.0
                  total_carbohydrates:
                    type: float
                    example: 50.0
                  day:
                    type: integer
                    example: 1
                  date:
                    type: string
                    format: date-time
                    example: "2025-01-01T08:00:00"
                  foods:
                    type: array
                    items:
                      type: object
                      properties:
                        food_id:
                          type: integer
                          example: 1
                        name:
                          type: string
                          example: "Huevos"
                        description:
                          type: string
                          example: "Huevos cocidos"
                        calories:
                          type: float
                          example: 70.0
                        proteins:
                          type: float
                          example: 6.0
                        fats:
                          type: float
                          example: 5.0
                        carbohydrates:
                          type: float
                          example: 1.0
                        quantity:
                          type: float
                          example: 2
                        type_quantity:
                          type: string
                          example: "Unidades"
                        category:
                          type: string
                          example: "Proteínas"
                        benefits:
                          type: string
                          example: "Fuente de proteínas"
                        image_url:
                          type: string
                          example: "https://example.com/huevos.jpg"
      404:
        description: No se encontró un plan activo para el usuario.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "No hay planes activos"
    """
    # Obtener el plan actual con status "en progreso"
    current_plan = Plan.query.filter_by(user_id=current_user_id, status="en progreso").first()
    
    if not current_plan:
        return jsonify({"error": "No hay planes activos"}), 404

    # Construir el JSON de respuesta
    response = {
        "plan_id": current_plan.id,
        "name": current_plan.name,
        "calories": current_plan.calories,
        "date_generation": current_plan.date_generation.isoformat(),
        "status": current_plan.status,
        "meals": []
    }
    
    # Obtener las comidas asociadas al plan
    for plan_meal in current_plan.plan_meal:
        meal = plan_meal.meal
        meal_data = {
            "meal_id": meal.id,
            "name": meal.name,
            "meal_type": meal.meal_type,
            "total_calories": meal.total_calories,
            "total_proteins": meal.total_proteins,
            "total_fats": meal.total_fats,
            "total_carbohydrates": meal.total_carbohydrates,
            "day": plan_meal.day,  # Día de la comida
            "date": plan_meal.date.isoformat(),  # Fecha de la comida
            "foods": []
        }

        # Obtener los alimentos asociados a la comida
        for meal_food in meal.meal_food:
            food = meal_food.food
            food_data = {
                "food_id": food.id,
                "name": food.name,
                "description": food.description,
                "calories": food.calories,
                "proteins": food.proteins,
                "fats": food.fats,
                "carbohydrates": food.carbohydrates,
                "quantity": meal_food.quantity,
                "type_quantity": meal_food.type_quantity,
                "category": food.category,
                "benefits": food.benefits,
                "image_url": food.image_url
            }
            meal_data["foods"].append(food_data)

        response["meals"].append(meal_data)

    return jsonify(response)

    # Obtener el plan actual con status "en progreso"
    current_plan = Plan.query.filter_by(user_id=current_user_id,status="en progreso").first()
    
    if not current_plan:
        return jsonify({"error": "Ho hay planes activos"}), 404

    # Construir el JSON de respuesta
    response = {
        "plan_id": current_plan.id,
        "name": current_plan.name,
        "calories": current_plan.calories,
        "date_generation": current_plan.date_generation.isoformat(),
        "status": current_plan.status,
        "meals": []
    }
    # Obtener las comidas asociadas al plan
    for plan_meal in current_plan.plan_meal:
        meal = plan_meal.meal
        meal_data = {
            "meal_id": meal.id,
            "name": meal.name,
            "meal_type": meal.meal_type,
            "total_calories": meal.total_calories,
            "total_proteins": meal.total_proteins,
            "total_fats": meal.total_fats,
            "total_carbohydrates": meal.total_carbohydrates,
            "day": plan_meal.day,  # Día de la comida
            "date": plan_meal.date.isoformat(),  # Fecha de la comida
            "foods": []
        }


        # Obtener los alimentos asociados a la comida
        for meal_food in meal.meal_food:
            food = meal_food.food
            food_data = {
                "food_id": food.id,
                "name": food.name,
                "description": food.description,
                "calories": food.calories,
                "proteins": food.proteins,
                "fats": food.fats,
                "carbohydrates": food.carbohydrates,
                "quantity": meal_food.quantity,
                "type_quantity": meal_food.type_quantity,
                "category": food.category,
                "benefits": food.benefits,
                "image_url": food.image_url
            }
            meal_data["foods"].append(food_data)

        response["meals"].append(meal_data)

    # Devolver la respuesta como JSON
    return jsonify(response), 200