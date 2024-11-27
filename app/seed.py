import os
from flask import Flask, request
import pandas as pd
import psycopg2
from datetime import datetime

from app.database import db
from app.models.physical_activity import PhysicalActivity
from app.models.user import User
from app.models.health_profile import HealthProfile
from app.models.food import Food


#función para cargar datos de tipos de actividad fisica predefinidas en la base de datos
def seed_data():
    # Datos predefinidos para PhysicalActivity
    activities = [
        {"name": "Sedentario", "description": "Poco o ningún ejercicio", "PAL": 1.2},
        {"name": "Ligeramente Activo", "description": "Ejercicio/deporte ligero 1-3 días a la semana", "PAL": 1.375},
        {"name": "Moderadamente Activo", "description": "Ejercicio/deporte moderado 3-5 días a la semana", "PAL": 1.55},
        {"name": "Muy Activo", "description": "Ejercicio/deporte intenso 6-7 días a la semana", "PAL": 1.725},
        {"name": "Extra Activo", "description": "Ejercicio muy intenso o trabajo físico", "PAL": 1.9}
    ]

    # Verificar e insertar solo si la actividad no existe
    for activity_data in activities:
        # Comprobar si ya existe una actividad con el mismo nombre
        existing_activity = PhysicalActivity.query.filter_by(name=activity_data['name']).first()
        
        # Si no existe, crear una nueva actividad
        if not existing_activity:
            activity = PhysicalActivity(
                name=activity_data['name'],
                description=activity_data['description'],
                PAL=activity_data['PAL']
            )
            db.session.add(activity)

    # Commit para guardar las actividades en la base de datos
    db.session.commit()

    print("Datos de actividad física predefinidos cargados exitosamente.")

#función para cargar datos de usuarios y perfiles de salud predefinidos en la base de datos
def seed_users_health_profile():
    # Datos predefinidos para User
    users = [
        {
            "name": "Juan",
            "lastname": "Pérez",
            "telephone": "555-1234",
            "email": "juan.perez@example.com",
            "password": "securepassword123",
            "url_image": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg",
            "health_profile": {
                "age": 30,
                "weight": 75.5,
                "height": 1.78,
                "physical_activity_id": 3,  # Moderadamente Activo
                "health_restrictions": "Ninguna",
                "birthday": datetime(1994, 5, 15),
                "gender": "Masculino",
            },
        },
        {
            "name": "María",
            "lastname": "López",
            "telephone": "555-5678",
            "email": "maria.lopez@example.com",
            "password": "mypassword123",
            "url_image": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg",
            "health_profile": {
                "age": 25,
                "weight": 62.0,
                "height": 1.65,
                "physical_activity_id": 2,  # Ligeramente Activo
                "health_restrictions": "Diabetes",
                "birthday": datetime(1999, 7, 20),
                "gender": "Femenino",
            },
        },
        {
            "name": "Carlos",
            "lastname": "Gómez",
            "telephone": "555-8765",
            "email": "carlos.gomez@example.com",
            "password": "password123",
            "url_image": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg",
            "health_profile": {
                "age": 40,
                "weight": 85.0,
                "height": 1.75,
                "physical_activity_id": 1,  # Sedentario
                "health_restrictions": "Hipertensión",
                "birthday": datetime(1984, 3, 12),
                "gender": "Masculino",
            },
        },
        {
            "name": "Ana",
            "lastname": "Torres",
            "telephone": "555-2468",
            "email": "ana.torres@example.com",
            "password": "anasecret123",
            "url_image": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg",
            "health_profile": {
                "age": 50,
                "weight": 90.0,
                "height": 1.70,
                "physical_activity_id": 1,  # Sedentario
                "health_restrictions": "Problemas articulares",
                "birthday": datetime(1974, 1, 5),
                "gender": "Femenino",
            },
        },
        {
            "name": "Luis",
            "lastname": "Ramírez",
            "telephone": "555-1357",
            "email": "luis.ramirez@example.com",
            "password": "luispass123",
            "url_image": "https://res.cloudinary.com/dnkvrqfus/image/upload/v1700017356/user_zmcosz.jpg",
            "health_profile": {
                "age": 35,
                "weight": 78.0,
                "height": 1.80,
                "physical_activity_id": 4,  # Muy Activo
                "health_restrictions": "Ninguna",
                "birthday": datetime(1989, 9, 10),
                "gender": "Masculino",
            },
        },
        {
            "name": "Carmen",
            "lastname": "Martínez",
            "telephone": "555-3579",
            "email": "carmen.martinez@example.com",
            "password": "carmenpass123",
            "url_image": "http://example.com/image6.jpg",
            "health_profile": {
                "age": 60,
                "weight": 70.0,
                "height": 1.60,
                "physical_activity_id": 2,  # Ligeramente Activo
                "health_restrictions": "Enfermedad cardíaca",
                "birthday": datetime(1964, 2, 22),
                "gender": "Femenino",
            },
        },
        {
            "name": "Eduardo",
            "lastname": "Fernández",
            "telephone": "555-6543",
            "email": "eduardo.fernandez@example.com",
            "password": "edupass123",
            "url_image": "http://example.com/image7.jpg",
            "health_profile": {
                "age": 45,
                "weight": 95.0,
                "height": 1.85,
                "physical_activity_id": 3,  # Moderadamente Activo
                "health_restrictions": "Sobrepeso",
                "birthday": datetime(1979, 12, 3),
                "gender": "Masculino",
            },
        },
        {
            "name": "Gloria",
            "lastname": "Sánchez",
            "telephone": "555-7412",
            "email": "gloria.sanchez@example.com",
            "password": "gloriaspass123",
            "url_image": "http://example.com/image8.jpg",
            "health_profile": {
                "age": 28,
                "weight": 55.0,
                "height": 1.62,
                "physical_activity_id": 4,  # Muy Activo
                "health_restrictions": "Bajo peso",
                "birthday": datetime(1996, 6, 18),
                "gender": "Femenino",
            },
        },
        {
            "name": "Ricardo",
            "lastname": "Vargas",
            "telephone": "555-8523",
            "email": "ricardo.vargas@example.com",
            "password": "ricardopass123",
            "url_image": "http://example.com/image9.jpg",
            "health_profile": {
                "age": 20,
                "weight": 70.0,
                "height": 1.75,
                "physical_activity_id": 5,  # Extra Activo
                "health_restrictions": "Ninguna",
                "birthday": datetime(2004, 11, 25),
                "gender": "Masculino",
            },
        },
        {
            "name": "Elena",
            "lastname": "Morales",
            "telephone": "555-9638",
            "email": "elena.morales@example.com",
            "password": "elenapass123",
            "url_image": "http://example.com/image10.jpg",
            "health_profile": {
                "age": 18,
                "weight": 50.0,
                "height": 1.55,
                "physical_activity_id": 3,  # Moderadamente Activo
                "health_restrictions": "Trastornos alimenticios",
                "birthday": datetime(2006, 4, 15),
                "gender": "Femenino",
            },
        },
    ]
     
    for user_data in users:
        # Crear usuario
        user = User(
            name=user_data["name"],
            lastname=user_data["lastname"],
            telephone=user_data["telephone"],
            email=user_data["email"],
            password=user_data["password"],
            url_image=user_data["url_image"],
        )
        db.session.add(user)
        db.session.commit()  # Guardar para obtener el ID del usuario

        # Crear perfil de salud
        health_profile_data = user_data["health_profile"]
        health_profile = HealthProfile(
            age=health_profile_data["age"],
            weight=health_profile_data["weight"],
            height=health_profile_data["height"],
            update_date=datetime.utcnow(),
            health_restrictions=health_profile_data["health_restrictions"],
            birthday=health_profile_data["birthday"],
            gender=health_profile_data["gender"],
            user_id=user.id,
            physical_activity_id=health_profile_data["physical_activity_id"],
        )
        db.session.add(health_profile)

        # Guardar todos los cambios
        db.session.commit()

        print("Usuarios y perfiles de salud cargados exitosamente.")

#función para cargar datos de alimentos predefinidos en la base de datos
def seed_food():
    base_dir = os.getcwd()  # Directorio base (raíz del proyecto)
    filepath = os.path.join(base_dir, 'templates', 'alimentos.xlsx')
    quantity = 0  # Contador de alimentos insertados

    # Verificar si el archivo existe
    if not os.path.exists(filepath):
        print(f"El archivo {filepath} no existe.")
        return

    try:
        # Leer el archivo Excel
        df = pd.read_excel(filepath)

        # Verificar que las columnas necesarias existan
        required_columns = ['nombre', 'descripcion', 'calorias', 'proteinas', 
                            'grasas', 'carbohidratos', 'imagen_url', 'categoria', 'beneficios']
        if not all(col in df.columns for col in required_columns):
            print(f"El archivo Excel no contiene las columnas necesarias: {required_columns}")
            return

        # Insertar datos en la tabla
        for index, row in df.iterrows():
            try:
                # Reemplazar las comas por puntos y convertir a float, ignorando valores nulos
                calories = float(str(row['calorias']).replace(',', '.')) if pd.notnull(row['calorias']) and row['calorias'] != 0 else None
                proteins = float(str(row['proteinas']).replace(',', '.')) if pd.notnull(row['proteinas']) and row['proteinas'] != 0 else None
                fats = float(str(row['grasas']).replace(',', '.')) if pd.notnull(row['grasas']) and row['grasas'] != 0 else None
                carbohydrates = float(str(row['carbohidratos']).replace(',', '.')) if pd.notnull(row['carbohidratos']) and row['carbohidratos'] != 0 else None
                
                # Crear el objeto Food
                food = Food(
                    name=row['nombre'],
                    description=row['descripcion'],
                    calories=calories if calories is not None else 0.0,  # Si es None, asignamos 0.0
                    proteins=proteins if proteins is not None else 0.0,  # Lo mismo para proteínas
                    fats=fats if fats is not None else 0.0,              # Y grasas
                    carbohydrates=carbohydrates if carbohydrates is not None else 0.0,  # Y carbohidratos
                    image_url=row['imagen_url'],
                    category=row['categoria'],
                    benefits=row['beneficios']
                )
                db.session.add(food)
                quantity += 1
            except Exception as e:
                print(f"Error al procesar fila {index}: {e}")

        # Guardar todos los cambios en la base de datos
        db.session.commit()
        print(f"Se han cargado {quantity} alimentos.")
    except Exception as e:
        print(f"Error al leer o insertar datos: {e}")