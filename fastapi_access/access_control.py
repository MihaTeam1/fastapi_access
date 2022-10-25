from fastapi import HTTPException, status, Depends
from typing import Optional, Callable

from .rule import Rule


class AccessDataProvider:
    @staticmethod
    def __call__():
        pass

    @classmethod
    def set_access_data_func(cls, new_function):
        cls.__call__ = staticmethod(new_function)


_access_data_provider = AccessDataProvider()


class AccessControl:
    def __init__(self, rules: Rule, message: Optional[str] = None):
        self.__rules = rules
        self.__message = message or 'Access denied'

    def __call__(self, data: dict = Depends(_access_data_provider)):
        if not self.__rules(data):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    'message': self.__message
                }
            )

    @staticmethod
    def set_access_data_func(new_function: Callable) -> None:
        _access_data_provider.set_access_data_func(new_function)


