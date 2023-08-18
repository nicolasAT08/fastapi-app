# FastAPI
from fastapi import Response, status, HTTPException, Depends, APIRouter

from typing import List, Optional

# Models (pydantic), schemas (postgres), DB connection, functions
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",  # Avoid to indicate the path operation root
    tags = ["Posts"]    # Create section in Swagger documentation
    )

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str]=""): # In postman {{URL}}posts?limit=3&skip=2 This is a query parameter. 10 is a default value
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # It print the amount the user of posts the user wants to see. Search parameter is optional because we don't want to pass a default str/serch
    
    # Add the votes to each post
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
                .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
                .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # Left Inner Join by default. We specify the Outter
    return posts

# Version to access only to user's posts
# @router.get("/", response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)): 
#     posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
#     return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
                .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
                .group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} was not found")
    
    return post

# Version to access only to user's posts
# @router.get("/{id}", response_model=schemas.Post)
# def get_post(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()
    
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} was not found")

#     if post.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action.')
    
#     return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)): 
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # The owner_id (from the model) is added here because this field is not requested to the user in the front-end
    db.add(new_post)  
    db.commit()  
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)  # Add .first() makes it a Post object. Without it is a <class 'sqlalchemy.orm.query.Query'>, so delete attribute (DB operation) below  works.
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action.') # Avoid users deleting others posts.
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    post_query =  db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action.')
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()

