from fastapi import HTTPException, status


def exception():
    raise HTTPException(status_code=404, detail="Record not found")


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
     )

    return credentials_exception

def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect user name or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return token_exception_response