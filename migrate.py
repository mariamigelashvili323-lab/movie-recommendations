from ext import app, db
from models import User, MovieCard, UserRecommendation

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database has been successfully reset and created!")