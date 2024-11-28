
# Requerimientos e Instalación

Este proyecto utiliza **Python**. Asegúrate de tenerlo instalado antes de comenzar.

## 1. Instalar el entorno virtual

Para crear un entorno virtual:

```bash
python -m venv venv
```

## 2. Activar el entorno virtual

Dependiendo de la terminal que utilices, activa el entorno virtual con uno de los siguientes comandos:

### Git Bash:

```bash
source venv/Scripts/activate
```

### Terminal de VSCode (Windows):

```bash
.\env\Scripts\ctivate
```

### Desactivar el entorno virtual

Para desactivar el entorno virtual en cualquier terminal:

```bash
deactivate
```

## 3. Instalar Flask

Con el entorno virtual activado, instala Flask:

```bash
pip install flask
```

## 4. Ejecutar la aplicación Flask

Para ejecutar la aplicación:

```bash
flask --app main --debug run --host=0.0.0.0
```

## 5. Instalar las dependencias

Con el entorno virtual activado y desde la raíz del proyecto, instala todas las dependencias:

```bash
pip install -r requirements.txt
```

Si no tienes el archivo `requirements.txt`, puedes instalar manualmente las dependencias con los siguientes comandos:

```bash
pip install SQLAlchemy
pip install flask_sqlalchemy
pip install psycopg2
pip install python-dotenv
pip install flask-httpauth
pip install pyjwt
pip install marshmallow-sqlalchemy
pip install flask-marshmallow
pip install Flask-migrate
pip install setuptools
pip install flasgger
```

## 6. Ejecutar migraciones

Para gestionar las migraciones de base de datos, utiliza los siguientes comandos:

### Inicializar migraciones (solo la primera vez):

```bash
flask db init
```

### Crear una nueva migración:

```bash
flask db migrate -m "detalle de la migración"
```

### Aplicar las migraciones:

```bash
flask db upgrade
```


## 7. Ejecutar comandos CLI

Este proyecto incluye varios comandos CLI registrados para facilitar la inicialización de datos en la base de datos. Se tiene que haber ejecutado las migraciones.

### Cargar datos de actividades físicas:

```bash
flask seed-physical-activities-db
```
Inicializa datos relacionados con actividades físicas en la base de datos.

### Cargar usuarios y perfiles de salud

```bash
flask seed-users-health-profiles-db
```
Inserta usuarios de ejemplo y sus respectivos perfiles de salud.

### Cargar alimentos predefinidos

```bash
flask seed-food-db
```
Agrega alimentos predefinidos con información detallada como calorías, proteínas y beneficios.

### Ejemplo de uso
Para poblar la base de datos con los datos iniciales, ejecuta uno o varios de estos comandos según sea necesario desde la raíz del proyecto:
```bash
flask seed-physical-activities-db
flask seed-users-health-profiles-db
flask seed-food-db

```

---

Este archivo `README.md` está estructurado para seguir las convenciones estándar y proporcionar una guía clara sobre cómo configurar y ejecutar el proyecto.
