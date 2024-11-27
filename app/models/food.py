from app.database import db

class Food(db.Model):
    __tablename__ = "food"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    proteins = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    benefits  = db.Column(db.String(255), nullable=False)

    # Relación con la tabla intermedia MealFood
    #meal_food_associations = db.relationship("MealFood", backref="food_association", cascade="all, delete-orphan")

    def __str__(self):
        return(
            f'id: {self.id}, '
            f'name: {self.name}, '
            f'description: {self.description}, '
            f'calories: {self.calories}, '
            f'proteins: {self.proteins}, '
            f'fats: {self.fats}, '
            f'carbohydrates: {self.carbohydrates}, '
            f'image_url: {self.image_url}, '
            f'category: {self.category}, '
            f'benefits: {self.benefits}'
        )