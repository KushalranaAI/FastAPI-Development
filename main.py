from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title:str
    content: str
    published: bool=True
    rating: Optional[int] = None

my_posts = [{"title":"welcome to goa", "content":"Beautiful place for solo and bachaler's", "id":2},{
    "title":"Welcome to delhi", "content":"Beautiful place for fast food lovers", "id":5
} ]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/")   #decorator method in python
async def root():
    return {"message": "My name is kushal rana. Upcoming Freelencer"}

# retrive all post
@app.get("/posts")
async def get_post():
    return {"post": my_posts}

## create a post
@app.post("/posts")
async def create_posts(post : Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# retrtive a single post using path parameter
@app.get("/posts/{id}")
async def get_post(id: int): # Validaton in FastAPI --> we have change over variable to suitable datatype
    post = find_post(id)     #because by default string is datatype of every request            
    print(post)
    return {"post details": post}
