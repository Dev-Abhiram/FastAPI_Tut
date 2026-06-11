from fastapi import FastAPI,Request,HTTPException,status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()
templates=Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

posts :list[dict]=[
    
        {
            "author":"John",
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
  },
  {
      "author":"John",
    "userId": 1,
    "id": 2,
    "title": "qui est esse",
    "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
  },
    
]

@app.get("/", include_in_schema=False,name="home")
@app.get("/posts", include_in_schema=False,name="posts")
def home(request: Request):
    limit = 3

    return templates.TemplateResponse(
        request,
        "home.html",
        context={
            "posts": posts[:limit],
            "title": "Home",
            "limit": limit,
            "has_more": len(posts) > limit
        }
    )

@app.get("/posts/{post_id}",include_in_schema=False)
def post_page(post_id:int,request:Request):
    for post in posts:
        if post.get("id","Not Found")==post_id:
            title=post['title'][:50]
            return templates.TemplateResponse(
            request,
            "post.html",
            context={
                "post": post,
                "title": "Home",
            }
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")


@app.get("/api/posts")
def get_posts():
  return posts

@app.get("/api/posts/{post_id}")
def get_post(post_id:int):
    for post in posts:
        if post.get("id","Not Found")==post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request:Request,exception:StarletteHTTPException):
    message=(exception.detail
        if exception.detail
        else "An error occured. Please check your request and try again" 
        )
    
    if request.url.path.startswith('/api'):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail":message}
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code":exception.status_code,
            "title":exception.status_code,
            "message":message,
        },
        status_code=  exception.status_code 
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request:Request,exception:RequestValidationError):
    if request.url.path.startswith('/api'):
         return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail":exception.errors()},
        )
    return templates.TemplateResponse(
    request,
    "error.html",
    {
        "status_code":status.HTTP_422_UNPROCESSABLE_ENTITY,
        "title":status.HTTP_422_UNPROCESSABLE_ENTITY,
        "message":"Invalid request. Please check your input and try again.",
    },
    status_code=  status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    







#################################################
@app.get("/login", name="login_page")
def login_page(request: Request):
    pass

@app.get("/register", name="register_page")
def register_page(request: Request):
    pass

@app.get("/account", name="account_page")
def account_page(request: Request):
    pass

@app.get("/users/{user_id}/posts", name="user_posts")
def user_posts(user_id: int):
    pass

@app.get("/user_id", name="user_id")
def user_id(request: Request):
    pass