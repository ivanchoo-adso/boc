from fastapi import FastAPI, Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

app = FastAPI()

outh2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username:str
    fullname:str
    email:str
    disabled:bool


class User_db(User):
    password:str

users_db = {
    "ivant":{
        "username": "ivanchoo",
        "fullname":"ivant",
        "email":"ivanfelipetabares@gmail.com",
        "disabled":False,
        "password":"123456",
    },
      "ivant2":{
        "username": "ivanchoo2",
        "fullname":"ivant",
        "email":"ivanfelipetabares@gmail.com",
        "disabled":True,
        "password":"654321",
    }
}

def search_user(username: str):
    if username in users_db:
        return User_db(**users_db[username])
    
async def current_user(token:str = Depends(outh2)):
    user = search_user(token)
    if not user:raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="credenciales de autentiacion invalidas", 
            headers={"WWW-Autenticate":"Bearer"})
    return user

@app.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username) 
    if not user_db:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto")

    user = search_user(form.username) 
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="La contrasena no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user
    
