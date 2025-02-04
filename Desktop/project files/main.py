from fastapi import FastAPI , Depends , HTTPException , status 
from sqlalchemy.orm import Session 
from pydantic import BaseModel 
from model import User , FoodItem , Dietplan, Base 
from database import SessionLocal , engine
from auth import hash_password, verify_password, create_access_token, verify_token, get_db 
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


app = FastAPI()

@app.get("/")
def home():
    return{"message" : "welcome to Diet Recommendation system"}

class UserLogin(BaseModel):
    username: str
    password: str    

class UserCreate(BaseModel):
    name : str
    email : str
    password : str
    age : int
    weight : float
    height : float  
    activity_level : str
    goal : str
    dietary_preference : str


class FoodItemCreate(BaseModel):
    name : str    
    calories : int
    protein : float
    carbs : float
    fats : float


class DietplanCreate(BaseModel):
    user_id : int
    food_id : int
    meal_type : str
    date : str




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already taken")
    
    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        age=user.age,
        weight=user.weight,
        height=user.height,
        activity_level=user.activity_level,
        goal=user.goal,
        dietary_preferences=user.dietary_preference
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}



# User login API (Token generation)
@app.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create JWT token if credentials are valid
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route to show user data
@app.get("/users/me/")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Validate and verify JWT token
    payload = verify_token(token)
    username: str = payload.get("sub")
    
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_user = db.query(User).filter(User.username == username).first()
    return db_user


# Add a protected route
@app.get("/user/{user_id}")
def get_user(user_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify token first
    payload = verify_token(token)
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



@app.post("/add_food_item/")
def add_food_item(food_item : FoodItemCreate , db : Session = Depends(get_db)):
    db_food_item = FoodItem(
        name=food_item.name,
        calories=food_item.calories,
        protein=food_item.protein,
        carbs=food_item.carbs,
        fats=food_item.fats
    )
    db.add(db_food_item)
    db.commit()
    db.refresh(db_food_item)
    return{"message" : "food item added successfully" , "food_id" : db_food_item.id}

@app.post("/create_diet_plan/")
def create_diet_plan(diet_plan: DietplanCreate, db: Session = Depends(get_db)):
    db_diet_plan = Dietplan (
        user_id=diet_plan.user_id,
        food_id=diet_plan.food_id,
        meal_type=diet_plan.meal_type,
        date=diet_plan.date
    )
    db.add(db_diet_plan)
    db.commit()
    db.refresh(db_diet_plan)
    return {"message": "Diet plan created successfully", "diet_plan_id": db_diet_plan.id}

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.get("/get_user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/food_items/")
def get_food_items(db: Session = Depends(get_db)):
    food_items = db.query(FoodItem).all()
    return food_items


@app.get("/diet_plans/")
def get_diet_plans(db: Session = Depends(get_db)):
    diet_plans = db.query(Dietplan).all()
    return diet_plans


@app.put("/update_user/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    db_user.age = user.age
    db_user.weight = user.weight
    db_user.height = user.height
    db_user.activity_level = user.activity_level
    db_user.goal = user.goal
    db_user.dietary_preferences = user.dietary_preferences

    db.commit()
    db.refresh(db_user)
    return {"message": "User updated successfully"}

