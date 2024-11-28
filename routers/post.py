from fastapi import APIRouter,Depends,HTTPException,status
import schemas,auth
from database import cursor,conn
router=APIRouter(prefix="/posts",tags=['posts'])
@router.post('/createPost',response_model=schemas.postCreation,status_code=status.HTTP_201_CREATED)
def createPosts(post:schemas.createPost,owner_id:int=Depends(auth.get_current_user)):
    cursor.execute("""INSERT INTO posts (title,content,owner_id) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,owner_id))
    new_post=cursor.fetchone()
    conn.commit()
    #get the owner info
    cursor.execute("""SELECT id,name,email FROM users WHERE id=%s;""",(owner_id,))
    owner=cursor.fetchone()
    #coonect post and owner
    return {"post":new_post,"owner":owner}
@router.get('/getPostById/{post_id}',response_model=schemas.postWithUserVote)
def getPostById(post_id:int,owner_id:int=Depends(auth.get_current_user)):
       cursor.execute("""SELECT posts.id,posts.title,posts.content,posts.created_at,posts.owner_id,users.email AS owner_email,users.name AS owner_name,COUNT(votes.post_id)  AS votes FROM  posts LEFT JOIN votes ON posts.id = votes.post_id LEFT JOIN users ON users.id=posts.owner_id WHERE posts.id=%s GROUP BY  posts.id ,users.id;""",(post_id,))
       post=cursor.fetchone()
       if post is None:
             raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{post_id} does not exist")
       return post
@router.get("/getAllPost",response_model=list[schemas.postWithUserVote])
def getAllPost(search:str="",skip:int=0,limit:int=100,owner_id:int=Depends(auth.get_current_user)):
    cursor.execute("""SELECT posts.id,posts.title,posts.content,posts.created_at,posts.owner_id,users.email AS owner_email,users.name AS owner_name,COUNT(votes.post_id) AS votes FROM  posts LEFT JOIN votes ON posts.id = votes.post_id LEFT JOIN users ON posts.owner_id=users.id WHERE posts.title LIKE %s GROUP BY  posts.id,users.id LIMIT %s OFFSET %s;""",(f"%{search}%",limit,skip))
    post=cursor.fetchall()
    if not post:
         raise HTTPException(status_code=status.HTTP_200_OK,detail="NO POSTS IN THERE")  
    return  post
@router.put("/updatePost/{post_id}",response_model=schemas.postOut)
def updatePost(postUpdate:schemas.postUpdate,post_id:int,owner_id:int=Depends(auth.get_current_user)):
    cursor.execute("""SELECT * FROM posts WHERE id=%s """,(post_id,))
    post=cursor.fetchone()
    if post:
        if post['owner_id']==owner_id:
            cursor.execute("""UPDATE posts SET title=%s,content=%s WHERE id=%s RETURNING *""",(postUpdate.title,postUpdate.content,post_id))
            new_post=cursor.fetchone()
            conn.commit()
            return new_post
        else:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="YOU ARE NOT A AUTHORISED PERSON TO UPDATE THIS POST")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"POST WITH ID :{post_id} DOES MOT EXIST")
@router.delete("/deletePost/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def deletePost(post_id:int,owner_id:int=Depends(auth.get_current_user)):
     cursor.execute("""SELECT * FROM posts WHERE id=%s""",(post_id,))
     post=cursor.fetchone()
     if post:
          if post['owner_id']==owner_id:
               cursor.execute("""DELETE FROM posts WHERE id=%s""",(post_id,))
               conn.commit()
               return f"POST WITH ID:{post_id} WAS DELETED SUCCESSFULLY"
          else:
               raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="YOU ARE NOT A AUTHORISED PERSON TO DELETE THIS POST")
     else:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"POST WITH ID:{post_id} DOES NOT EXIST ")




    
