#REQUERIMIENTOS E INSTALACION



Tener instalado python en la computadora

#1. Instalar entorno virtual
python -m venv venv

#2. Levantar el entorno virtual
source venv/Scripts/activate (git bash)
o
.\venv\Scripts\activate (terminal VScode)

#SI SE DESEA DESACTIVAR EL ENTORNO VIRTUAL, ingresar "deactivate" ubicado en la raíz del proyecto

#3. Levantado el entorno virtual, instalar flask
pip install flask

#4. Levantar flask 
flask --app main --debug run

#5. Instalar librerías (ubicado en la raiz, con el entorno activado)
pip install -r requirements.txt
 o 

pip install SQLAlchemy
pip install flask_sqlalchemy
pip install psycopg2
pip install python-dotenv

pip install flask-httpauth
pip install pyjwt
pip install marshmallow-sqlalchemy
pip install Flask-migrate
pip install -U setuptools
pip install flasgger


#6 Ejecutar las migraciones
en una nueva terminal con el entorno virtual levantado, ejecutar:
flask db init (la primera vez en migrar)
flask db migrate -m "detalle de la migracion" (similar a git commit)
flask db upgrade (similar a git push)


Endpoints (swagger)
http://localhost:5000/apidocs/
