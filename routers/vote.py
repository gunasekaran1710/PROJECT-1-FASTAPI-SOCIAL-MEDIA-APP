from fastapi import APIRouter,Depends,HTTPException,status
from auth import get_current_user
import database,schemas
from database import cursor,conn
router=APIRouter(prefix="/votes",tags=['votes'])
@router.post('/')
def createVotes(votes:schemas.Votes,owner_id:int=Depends(get_current_user)):
  cursor.execute("""SELECT * FROM posts WHERE id=%s""",(votes.post_id,))
  post=cursor.fetchone()
  if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{votes.post_id} does not exist")
  else:
     if votes.direction==1:
         try:
           cursor.execute("""INSERT INTO votes(user_id,post_id) VALUES (%s,%s);""",(owner_id,votes.post_id) )
           conn.commit()
           return f"successfully voted in post_id:{votes.post_id} by the user id {owner_id}"
         except Exception as error:
            conn.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"vote is already exist on post_id:{votes.post_id} by user_id:{owner_id}")
     elif votes.direction==0:
          cursor.execute("""SELECT * FROM votes WHERE user_id=%s AND post_id=%s""",(owner_id,votes.post_id))
          vote=cursor.fetchone()
          if vote is None:
             raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f" there is no vote exist on post_id:{votes.post_id} by user_id:{owner_id}")
          cursor.execute("""DELETE FROM votes WHERE user_id=%s AND post_id=%s""",(owner_id,votes.post_id))
          conn.commit()
          raise HTTPException(status_code=status.HTTP_200_OK,detail=f"unvoted successfully in post_id:{votes.post_id} by the user_id:{owner_id}") 
     else :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"choose the corect direction":{"1":"add vote","0":"delete the added vote"}})

