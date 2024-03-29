import sys
# sys.path.append("..")

from typing import Optional
from fastapi import Depends, APIRouter, Form, HTTPException, Request, Response, status
from exception import get_user_exception, token_exception
from request_body import UsersDetailsSchema
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import models

SECRET_KEY = "AMITKUMARSAHI24101997"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={401: {"user": "Not authorised"}}
)


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_outh_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(user_name: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.user_name == user_name).first()

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            logout(request)
        return {"user_name": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="Not Found")


@router.post('/create/user')
async def create_user(details: UsersDetailsSchema, db: Session = Depends(get_db)):
    user = models.Users()
    user.user_name = details.user_name
    user.first_name = details.first_name
    user.last_name = details.last_name
    user.email = details.email
    user.password = get_password_hash(details.password)
    user.is_active = True
    db.add(user)
    db.commit()
    print("done----------->")


@router.post("/token")
async def get_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return False
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.user_name, user.id, expires_delta=token_expires)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return True


@router.get('/', response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post('/', response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_outh_form()
        response = RedirectResponse(url='/todos/home', status_code=status.HTTP_302_FOUND)
        validate_user_cookie = await get_access_token(response=response, form_data=form, db=db)
        if not validate_user_cookie:
            msg = "Incorrect username or password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response
    except HTTPException:
        msg = "Unknown error"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.get("/logout")
async def logout(request: Request):
    msg = "Log out successfully"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response


@router.get('/register', response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post('/register', response_class=HTMLResponse)
async def register_user(
        request: Request,
        email: str = Form(...),
        username: str = Form(...),
        firstname: str = Form(...),
        lastname: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)):
    validation1 = db.query(models.Users).filter(models.Users.user_name == username).first()
    validation2 = db.query(models.Users).filter(models.Users.email == email).first()
    if validation1 is not None or validation2 is not None:
        msg = "Invalid registration request"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})
    record = models.Users()
    record.user_name = username
    record.email = email
    record.first_name = firstname
    record.last_name = lastname
    record.password = get_password_hash(password)
    record.is_active = True
    db.add(record)
    db.commit()
    msg = "Registration completed!"
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
