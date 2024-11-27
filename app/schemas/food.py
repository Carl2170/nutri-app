from app.extensions import ma
from app.models.food import Food

class FoodSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Food
        include_relationships = True
        load_instance = True  # Permite deserializar a un objeto Food