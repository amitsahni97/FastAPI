# import sys
# sys.path.append("..")

from fastapi import APIRouter, Depends, Form, Request
from request_body import UsersDetailsSchema
from request_body import TodoRequestSchema
from exception import exception, get_user_exception
from database import SessionLocal, engine
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette import status



import models
from sqlalchemy.orm import Session
from routers import auth

# from auth import get_current_user
router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
    responses={404: {"description": "Not found"}}
)
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

# app.include_router(auth.router)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/home', response_class=HTMLResponse)
async def test_home(request: Request, db: Session = Depends(get_db)):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    todos = db.query(models.Todos).filter(models.Todos.owner_id == user.get("user_id")).all()
    return templates.TemplateResponse("home.html", {"request": request, "todos": todos, "user":user})


@router.get('/add-todo', response_class=HTMLResponse)
async def test_add_todo(request: Request):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add-todo.html", {"request": request , "user":user})


@router.post('/add-todo', response_class=HTMLResponse)
async def create_todo(
    request:Request,
    title: str = Form(...),
    description: str = Form(...),
    priority:int = Form(...),
    db: Session = Depends(get_db)
    ):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    record = models.Todos()
    record.title = title
    record.description = description
    record.priority = priority
    record.owner_id = user.get("user_id")
    record.complete = False
    db.add(record)
    db.commit()
    return RedirectResponse(url="/todos/home", status_code=status.HTTP_302_FOUND)



@router.get('/edit-todo', response_class=HTMLResponse)
async def test_add_todo(request: Request):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("edit-todo.html", {"request": request, "user":user})



@router.get('/')
async def read_all(db: Session = Depends(get_db)):
    """
    Function to get all the details present in table
    """
    return db.query(models.Todos).all()


@router.get('/')
async def read_by_user(
    user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
    ):
    """
    Function to get all the record present in TODO table
    """
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()


@router.get('/{todo_id}')
async def get_detail(todo_id: int, user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """
    Function to get details of specific id
    """
    if user is None:
        raise get_user_exception()
    record = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id==user.get("id")).first()
    if record is not None:
        return record
    raise exception()


@router.post('/post')
async def post_body(data: TodoRequestSchema, user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if user is None:
        return get_user_exception()
    record = models.Todos()
    record.title = data.title
    record.description = data.description
    record.priority = data.priority
    record.complete = data.complete
    record.owner_id = user.get("user_id")
    db.add(record)
    db.commit()
    return {
        'status': 201,
        'transaction': 'success'
    }


@router.delete('/delete/{todo_id}')
async def delete_record(request: Request, todo_id: int, db: Session = Depends(get_db)):
    """
    Function to delete the record of TODO table based on id given
    :param todo_id: int
    :param db: object
    :return int
    """
    print("1---------")
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    record = db.query(models.Todos).filter(models.Todos.id == todo_id).\
        filter(models.Todos.owner_id == user.get("user_id")).first()
    print("here------>")
    if record is None:
        return RedirectResponse(url="/todos/home", status_code=status.HTTP_302_FOUND)
    
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
    return RedirectResponse(url="/todos/home", status_code=status.HTTP_302_FOUND)
