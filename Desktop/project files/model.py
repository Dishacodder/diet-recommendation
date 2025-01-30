from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key=True , index = True)
    name = Column(String , nullable=False)
    email = Column(String ,unique=True , nullable=False)
    password = Column(String , nullable=False)
    age = Column(Integer, nullable=True)  
    weight = Column(Integer, nullable=True)  
    height = Column(Integer, nullable=True)  
    activity_level = Column(String, nullable=True) 
    goal = Column(String, nullable=True) 
    dietary_preferences = Column(String, nullable=True) 



class FoodItem(Base):
    __tablename__ = "food_items"
    id = Column(Integer ,primary_key=True , index=True)
    name = Column(String , nullable = False)
    calories = Column(Integer , nullable = False)  
    protein = Column(Integer, nullable=True)  
    carbs = Column(Integer, nullable=True)  
    fats = Column(Integer, nullable=True)  
  

class Dietplan(Base):
    __tablename__ = "diet_plans"
    id = Column(Integer ,primary_key=True , index=True)
    user_id = Column(Integer , ForeignKey("users.id") , nullable=False)
    food_id = Column(Integer , ForeignKey("food_items.id") , nullable = False)
    meal_type = Column(String , nullable = False)    
    date = Column(String, nullable=True) 
