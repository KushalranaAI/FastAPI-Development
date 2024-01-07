from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
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



def find_post(id):  ## find a post ina my posts list
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):   ## find a item in a list that required and return it's index
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i



@app.get("/")   #decorator method in python
async def root():
    return {"message": "My name is kushal rana. Upcoming Freelencer"}

# retrive all post
@app.get("/posts")
async def get_post():
    return {"post": my_posts}

## create a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)  ## set by default a status code of create in 201
async def create_posts(post : Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# retrive a single post using path parameter
@app.get("/posts/{id}")
async def get_post(id: int, response: Response): # Validaton in FastAPI --> we have change over variable to suitable datatype
                              #because by default string is datatype of every request    
    post = find_post(id)   
    if not post:
        # response.status_code =  status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} is not found"}   
        # we can replace above two line with simple version
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} is not found")
    return {"post details": post}



# delete a post 
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id:{id} is not exist")
        
    my_posts.pop(index)
    return Response(status_code= status.HTTP_204_NO_CONTENT)


# update post
@app.put("/posts/{id}")
async def update_post(id: int, update_post:Post):
    
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id:{id} is not exist")
        
    update_post_dict = update_post.dict()
    update_post_dict['id'] = id
    my_posts[index] = update_post_dict
    return {"message": update_post_dict}