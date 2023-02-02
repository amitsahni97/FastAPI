from fastapi import FastAPI, Depends, HTTPException
from request_body import TodoRequestSchema
from exception import exception
from database import SessionLocal, engine
import models
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.get('/todo/{todo_id}')
async def get_detail(todo_id: int, db: Session = Depends(get_db)):
    record = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if record is not None:
        return record
    raise exception()


@app.post('/todo/post')
async def post_body(data: TodoRequestSchema, db: Session = Depends(get_db)):
    record = models.Todos()
    print("id--->", data.id)
    print("-------------------")
    record.id = data.id
    record.title = data.title
    record.description = data.description
    record.priority = data.priority
    record.complete = data.complete
    print("record complete---->", record.complete)

    db.add(record)
    db.commit()
    return {
        'status': 201,
        'transaction': 'success'
    }
