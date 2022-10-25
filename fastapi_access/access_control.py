from fastapi import HTTPException, status, Depends, FastAPI
from typing import Optional, Callable

from .rule import Rule


def get_access_data():
    pass


class AccessControl:
    def __init__(self, rules: Rule, message: Optional[str] = None):
        self.__rules = rules
        self.__message = message or 'Access denied'

    def __call__(self, data: dict = Depends(get_access_data)):
        if not self.__rules(data):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    'message': self.__message
                }
            )

    @staticmethod
    def set_access_data_func(app: FastAPI, new_function: Callable) -> None:
        app.dependency_overrides[get_access_data] = new_function


