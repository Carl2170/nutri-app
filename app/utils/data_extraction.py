from app.utils.nutrion_model import get_food_data
from app.database import create_engine
import pandas as pd
import unittest

class TestFoodDataExtraction(unittest.TestCase):

    def test_get_food_data(self):
        # Crear la conexión con la base de datos
        engine = create_engine('postgresql://postgres:Eyeoftiger123@localhost:5432/nutri_app')

        # Obtener los datos de los alimentos
        food_data = get_food_data()

        # Verificar que el DataFrame contiene las columnas esperadas
        expected_columns = ['name', 'calories', 'proteins', 'fats', 'carbohydrates']
        for col in expected_columns:
            self.assertIn(col, food_data.columns, f"La columna '{col}' falta en los datos de alimentos.")
        
        # Verificar que los datos no están vacíos
        self.assertGreater(len(food_data), 0, "No se han encontrado alimentos en la base de datos.")
