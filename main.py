from fastapi import FastAPI, Depends
from database import engine
import models
from routers import auth, todos
from starlette.staticfiles import StaticFiles
# from company import companyapis, dependencies

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(todos.router)

# app.include_router(
#     companyapis.router,
#     prefix="/companyApi",
#     tags=["CompanyApi"],
#     dependencies=[Depends(dependencies.get_token_header)],
#     responses={418: {"description": "Internal use only"}}
#     )
