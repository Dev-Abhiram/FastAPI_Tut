from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates=Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

posts :list[dict]=[
    
        {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
  },
  {
    "userId": 1,
    "id": 2,
    "title": "qui est esse",
    "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
  },
    
]

@app.get("/", include_in_schema=False,name="home")
@app.get("/posts", include_in_schema=False)
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


@app.get("/api/posts")
def get_posts():
  return posts
@app.get("/login", name="login_page")
def login_page(request: Request):
    pass

@app.get("/register", name="register_page")
def register_page(request: Request):
    pass

@app.get("/account", name="account_page")
def account_page(request: Request):
    pass