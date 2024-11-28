from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone
from fastapi import HTTPException,status,Depends
from database import cursor,conn
oauth2_schema=OAuth2PasswordBearer(tokenUrl='token')
import jwt
ASSESS_TOKEN_EXPIRE_MINUTES=10
SECREAT_KEY="VERY VERY SECRET"
ALGORITHM_USED="HS256"
credential_exception=HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="INVALID CREDENTIALS")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#HASHING FUNCTIONS
def hashing(password):
    hashed_password=pwd_context.hash(password)
    return hashed_password
def verify_password(password,hashed_password):
    verify_password=pwd_context.verify(password,hashed_password)
    return verify_password
#TOKEN GENERATE FUNCTION
def create_assess_token(data):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ASSESS_TOKEN_EXPIRE_MINUTES)
    to_encoded=data.copy()
    to_encoded.update({"exp":expire})
    print(to_encoded)
    jwt_token=jwt.encode(to_encoded,SECREAT_KEY,algorithm=ALGORITHM_USED)
    return jwt_token
#VERIFY ACCESS TOKEN
def verify_assess_token(token):
    try:
        jwt_token_verify=jwt.decode(token,SECREAT_KEY,algorithms=[ALGORITHM_USED])
        currentUser=cursor.execute("""SELECT * FROM users WHERE id=%s""",(jwt_token_verify['user_id'],))
        current_user=cursor.fetchone()
        if current_user is None:
             raise credential_exception
        return(jwt_token_verify['user_id'])
    except jwt.ExpiredSignatureError:
        raise credential_exception
#get current user
def get_current_user(token:str=Depends(oauth2_schema)):
        user=verify_assess_token(token)
        return user



