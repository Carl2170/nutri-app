from datetime import datetime
from flask import Blueprint, jsonify, request

from app.database import db
from app.models.food import Food

food_bp = Blueprint("food", __name__,  url_prefix="/api/food")

@food_bp.route("/foods", methods=["GET"])
def get_all_foods():
    """
    Obtener todos los alimentos
    ---
    tags:
      - Alimentos
    responses:
      200:
        description: Lista de todos los alimentos.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "Manzana"
              description:
                type: string
                example: "Fruta fresca y dulce, rica en fibra y vitaminas."
              calories:
                type: float
                example: 52
              proteins:
                type: float
                example: 0.3
              fats:
                type: float
                example: 0.2
              carbohydrates:
                type: float
                example: 14
              image_url:
                type: string
                example: "https://example.com/images/manzana.jpg"
              category:
                type: string
                example: "frutas"
              benefits:
                type: string
                example: "Ayuda a mantener el sistema digestivo saludable."
    """
    foods = Food.query.all()
    result = [
        {
            "id": food.id,
            "name": food.name,
            "description": food.description,
            "calories": food.calories,
            "proteins": food.proteins,
            "fats": food.fats,
            "carbohydrates": food.carbohydrates,
            "image_url": food.image_url,
            "category": food.category,
            "benefits": food.benefits
        }
        for food in foods
    ]
    return jsonify(result), 200

@food_bp.route('/foods/category/<string:category>', methods=['GET'])
def get_foods_by_category(category):
    foods = Food.query.filter_by(category=category).all()
    if not foods:
        return jsonify({"error": "No se encontraron alimentos para la categoría especificada"}), 404

    result = [
        {
            "id": food.id,
            "name": food.name,
            "description": food.description,
            "calories": food.calories,
            "proteins": food.proteins,
            "fats": food.fats,
            "carbohydrates": food.carbohydrates,
            "image_url": food.image_url,
            "category": food.category,
            "benefits": food.benefits
        }
        for food in foods
    ]
    return jsonify(result), 200

@food_bp.route('/foods/<int:id>', methods=['GET'])
def get_food_by_id(id):
    """
    Obtener un alimento por ID
    ---
    tags:
      - Alimentos
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID del alimento.
        example: 1
    responses:
      200:
        description: Detalles del alimento especificado.
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "Manzana"
            description:
              type: string
              example: "Fruta fresca y dulce, rica en fibra y vitaminas."
            calories:
              type: float
              example: 52
            proteins:
              type: float
              example: 0.3
            fats:
              type: float
              example: 0.2
            carbohydrates:
              type: float
              example: 14
            image_url:
              type: string
              example: "https://example.com/images/manzana.jpg"
            category:
              type: string
              example: "frutas"
            benefits:
              type: string
              example: "Ayuda a mantener el sistema digestivo saludable."
      404:
        description: Alimento no encontrado.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Alimento no encontrado."
    """
    food = Food.query.get(id)
    if not food:
        return jsonify({"error": "Alimento no encontrado"}), 404

    result = {
        "id": food.id,
        "name": food.name,
        "description": food.description,
        "calories": food.calories,
        "proteins": food.proteins,
        "fats": food.fats,
        "carbohydrates": food.carbohydrates,
        "image_url": food.image_url,
        "category": food.category,
        "benefits": food.benefits
    }
    return jsonify(result), 200