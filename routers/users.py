import schemas,auth
from fastapi import HTTPException,status,APIRouter,Depends
from database import conn,cursor
router=APIRouter(prefix="/user",tags=['USERS'])
@router.post("/createUser",status_code=status.HTTP_201_CREATED,response_model=schemas.user_out)
def userCreation(user:schemas.users):
       try:
         hashed_password=auth.hashing(user.password)
         cursor.execute("""INSERT INTO USERS(name,email,password) VALUES(%s,%s,%s) RETURNING *;""",(user.name,user.email,hashed_password))
         new_user=cursor.fetchone()
         conn.commit()
         return new_user
       except Exception as error:
           conn.rollback()
           raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"{user.email} is already exist")
@router.post("/login",status_code=status.HTTP_200_OK,response_model=schemas.assessToken)
def loginUser(user:schemas.loginUser):
    cursor.execute("""SELECT * FROM users WHERE email=%s ;""",(user.email,))
    user1=cursor.fetchone()
    if user1:
       verify_password=auth.verify_password(user.password,user1["password"])
       if verify_password is True:
           create_assess_token=auth.create_assess_token({"user_id":user1["id"]})
           return {"access_token":create_assess_token,"token_type":"bearer"}
       else:
           raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="INVALID CREDENTIALS")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="INVALID CREDENTIALS")
@router.delete("/delete")
def deleteUser(user:schemas.loginUser):
    cursor.execute("""SELECT * FROM users WHERE email=%s ;""",(user.email,))
    user1=cursor.fetchone()
    if user1:
       verify_password=auth.verify_password(user.password,user1["password"])
       if verify_password is True:
           cursor.execute("""DELETE FROM users WHERE email=%s""",(user.email,))
           conn.commit()
           raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
       else:
           raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="INVALID CREDENTIALS")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="INVALID CREDENTIALS") 
@router.put("/changeUsername",response_model=schemas.user_out)
def changeUsername(newuserName:schemas.userNameChange,user_id:int=Depends(auth.get_current_user)):
          change=cursor.execute("""UPDATE users SET name=%s WHERE id=%s ;""",(newuserName.new_userName,user_id))
          result=conn.commit()
          newUser=cursor.execute("""SELECT id,email,name FROM users WHERE id=%s;""",(user_id,))
          new_user=cursor.fetchone()
          return new_user
@router.get("/getAllUser",response_model=list[schemas.user_out])
def getAllUser(user_id:int=Depends(auth.get_current_user)):
    cursor.execute("""SELECT id,name,email FROM users;""")
    allUsers=cursor.fetchall()
    return allUsers
