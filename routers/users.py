import sys
sys.path.append('..')

from starlette import status
from starlette.responses import RedirectResponse

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user, get_password_hash, verify_password

templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/user",
    tags=['user'],
    responses={404: {"User": "Not verified"}}
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/change-pass", response_class=HTMLResponse)
async def change_password(request: Request):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("change-pass.html", {"request": request, 'user':user})

@router.post("/change-pass", response_class=HTMLResponse)
async def change_password(request: Request,
                          username: str = Form(),
                          password: str = Form(),
                          new_password1: str = Form(),
                          new_password2: str = Form(),
                          db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
    verification1 = user_model.username == username
    verification2 = verify_password(password, user_model.hashed_password)
    if not verification1 or not verification2:
        msg = "Username or password is incorrect"
        return templates.TemplateResponse("change-pass.html", {"request": request, "msg": msg})
    if new_password1 != new_password2:
        msg = "New Passwords do not match"
        return templates.TemplateResponse("change-pass.html", {"request": request, "msg": msg})

    user_model.hashed_password = get_password_hash(new_password1)
    db.add(user_model)
    db.commit()
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)