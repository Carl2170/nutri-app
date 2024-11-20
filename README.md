
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
.env\Scriptsctivate
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

## Documentación de Endpoints (Swagger)

Después de iniciar la aplicación Flask, puedes acceder a la documentación Swagger en la siguiente URL:

[http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)

---

Este archivo `README.md` está estructurado para seguir las convenciones estándar y proporcionar una guía clara sobre cómo configurar y ejecutar el proyecto.
