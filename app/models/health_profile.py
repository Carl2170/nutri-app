from app.database import db


class HealthProfile(db.Model):
    __tablename__ = "health_profile"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    physical_activity = db.Column(db.String(50), nullable=False)
    update_date = db.Column(db.DateTime, nullable=False)
    health_restrictions = db.Column(db.String(50), nullable=True)
    birthday = db.Column(db.Date, nullable=False)  # Campo de fecha
    gender = db.Column(db.String(10), nullable=False)  # Campo de género

    # Clave foránea que apunta a la tabla 'user'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    user = db.relationship('User', back_populates='health_profile')

    health_objectives = db.relationship('HealthObjective', backref='health_profile')

    def __str__(self):
        return(
            f'id: {self.user_id}, '
            f'Age: {self.age}, '
            f'Weight: {self.weight}, '
            f'physical_activity: {self.physical_activity}, '
            f'update_date: {self.update_date}'
            f'Gender: {self.gender}, '
            f'Birthday: {self.birthday}, '
        )

#CONDICION FISICA

# Sedentario

# Descripción: Realiza poco o ningún ejercicio físico. Su actividad diaria es mínima.
# Actividad Ligera

# Descripción: Realiza actividades ligeras como caminar ocasionalmente o hacer tareas domésticas.
# Actividad Moderada

# Descripción: Realiza ejercicio moderado 1-3 días a la semana (ejemplo: caminar, yoga, ciclismo ligero).
# Actividad Intensa

# Descripción: Realiza ejercicio intenso 3-5 días a la semana (ejemplo: correr, entrenamiento de fuerza, deportes).
# Atleta

# Descripción: Entrenamiento regular y intensivo, 6-7 días a la semana. Incluye deportes competitivos o entrenamiento especializado.

#RESTRICCION DE SALUD
# Ninguna
# Diabetes
# Hipertensión
# Asma
# Alergias (especificar)
# Enfermedad cardíaca
# Problemas articulares (especificar)
# Sobrepeso
# Bajo peso
# Trastornos alimenticios
# Problemas de movilidad
# Enfermedades respiratorias
# Cáncer (especificar)
# Enfermedades neurológicas
# Trastornos psicológicos (especificar)
# Limitaciones físicas (especificar)