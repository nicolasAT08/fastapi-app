from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from.. import database, schemas, models, utils, oauth2

# Step - 34 Add the authentication path operation
router = APIRouter(tags=['Authentication'],
                   prefix='/login')

@router.post("/", response_model=schemas.Token)
#def login(user_credentials:schemas.UserLogin, db:Session=Depends(database.get_db)):
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)): 
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() # When comparing from the OAuth2PasswordRequestForm, the email doesn't exist but {"username":"fgsdfg", "password":"hsdlkfha"} 
                                                                                            # In Postman we have to do the POST method using "form-data"
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials.')
    
    if not utils.verify(user_credentials.password, user.password): # Compare the pwd recieved from the user and the one in the DB
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials.')
    
    # Create a token
    access_token = oauth2.crate_access_token(data={"user_id":user.id}) # The data decided to put in the payload. https://jwt.io/ to decode the access_token

    return {"access_token":access_token, "token_type":"bearer"}