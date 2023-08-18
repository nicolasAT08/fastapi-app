# FastAPI
from fastapi import Response, status, HTTPException, Depends, APIRouter

from typing import List

# Models (pydantic), schemas (postgres), DB connection, functions
from .. import models, schemas, utils # Step 27 for schemas - 31 for utils
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users", # Avoid to indicate the operation root path
    tags=["Users"]      # Create section in Swagger documentation
    )  


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user:schemas.UserCreate,db: Session= Depends(get_db)):

    # Hash the user password - user.password pydantic model.
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} does not exist")
    
    return user

@router.get("/", response_model=List[schemas.User])
def get_posts(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int, db:Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} does not exist")
    
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.User)
def update_user(id:int, updated_user:schemas.UserCreate, db:Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} does not exist")
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()

    return user_query.first()