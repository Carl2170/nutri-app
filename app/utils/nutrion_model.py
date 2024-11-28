import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from app.database import db
from app.models.food import Food


engine = create_engine('postgresql://postgres:Eyeoftiger123@localhost:5432/nutri_app')

def get_user_data():
    # Lógica para obtener datos del usuario desde la base de datos (por ejemplo)
    user = db.get_user_data()
    return user


def get_food_data():
    # Obtener los alimentos y sus características (calorías, nutrientes, etc.)
    foods = Food.query.all()
    food_data = [
        {
            "name": food.name,
            "calories": food.calories,
            "proteins": food.proteins,
            "fats": food.fats,
            "carbohydrates": food.carbohydrates,
        }
        for food in foods
    ]
    return pd.DataFrame(food_data)

def train_nutrition_model(user_data):
    # Preprocesar los datos del usuario (peso, altura, etc.)
    X = user_data[['age', 'weight', 'height', 'activity_level']]  # Características del usuario
    y = user_data['calories']  # Calorías necesarias

    # Estandarizar los datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Entrenar el modelo de regresión lineal
    model = LinearRegression()
    model.fit(X_scaled, y)

    return model

def predict_calories_for_user(user_data, model):
    # Predecir las calorías necesarias para un nuevo usuario
    X_scaled = StandardScaler().fit_transform(user_data[['age', 'weight', 'height', 'activity_level']])
    predicted_calories = model.predict(X_scaled)
    return predicted_calories
