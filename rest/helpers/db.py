from functools import wraps
from typing import Any, Callable
from sqlalchemy import Engine
from sqlmodel import Session
from rest.extensions.db import engine


def get_engine() -> Engine:
    return engine

def get_session(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if "session" in kwargs:
            return func(*args, **kwargs)
        with Session(get_engine()) as session:
            kwargs["session"] = session
            return func(*args, **kwargs)
    return wrapper