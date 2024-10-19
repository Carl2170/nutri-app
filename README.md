#REQUERIMIENTOS E INSTALACION
Tener instalado python en la computadora

#1. Instalar entorno virtual
python -m venv venv

#2. Levantar el entorno virtual
source venv/Scripts/activate
o
.venv/Scripts/activate 

#SI SE DESEA DESACTIVAR EL ENTORNO VIRTUAL, ingresar "deactivate" ubicado en la raíz del proyecto

#3. Levantado el entorno virtual, instalar flask
pip install flask

#4. Levantar flask 
flask --app main --debug run

#5. Instalar librerías
pip install SQLAlchemy
pip install flask_sqlalchemy
pip install psycopg2
pip install python-dotenv

