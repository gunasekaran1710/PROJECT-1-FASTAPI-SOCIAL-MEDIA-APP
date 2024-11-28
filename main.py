from fastapi import FastAPI
from routers import users,post,vote
app=FastAPI()
app.include_router(users.router)
app.include_router(post.router)
app.include_router(vote.router)


