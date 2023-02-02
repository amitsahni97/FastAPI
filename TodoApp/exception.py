from fastapi import HTTPException


def exception():
    raise HTTPException(status_code=404, detail="Record not found")