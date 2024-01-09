from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

router=APIRouter(prefix="/user", 
                 tags=["user"],
                 responses={404: {"message": "No encontrado"}})

class User(BaseModel):
    id:int
    name:str
    apellidos:str
    url:str
    age:int

users_list = [User(id=1,name="Iván",apellidos="Tabares",url="https://ivant.com",age=19),
              User(id=2,name="felipe",apellidos="Tabares",url="https://ivant.com",age=20),
              User(id=3,name="Natalia",apellidos="Tabares",url="https://ivant.com",age=21)]


@router.get("/usersjson")
async def usersjson():
    return [{"name": "Iván", "apellidos":"Tabares","url": "https://ivant.com", "age": 35},
            {"name": "Iván2", "apellidos":"Tabares","url": "https://ivant.com, ", "age": 31},
            {"name": "Iván3", "apellidos":"Tabares","url": "https://ivant.com, ", "age": 32}]

@router.get("/")
async def users():
    return users_list

@router.get("/{id}")
async def user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"no se ha encontrado el usuario"}
    

@router.get("/")
async def user(id:int):
    return search_user(id)


def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"no se ha encontrado el usuario"}

@router.post("/",response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")       
    users_list.append(user)
    return user
        

@router.put("/")
async def user(user : User):
    found=False
    for index,save_user in enumerate(users_list):
        if save_user.id == user.id:
            users_list[index] = user
            found=True
    if not found:
        return{"error":"No se ha actualizado el usuario"}
    else:
        return user

@router.delete("/{id}")
async def user(id:int):

    found = False

    for index,save_user in enumerate(users_list):
        if save_user.id == id:
            del users_list[index]
            found=True
    if not found:
        return{"error":"No se ha eliminado el usuario"}
    else:
        return {"Se ha eliminado el usuario"} 
            