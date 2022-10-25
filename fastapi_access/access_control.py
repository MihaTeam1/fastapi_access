

class AccessDataProvider:

    @staticmethod
    def __call__():
        pass

    @classmethod
    def set_access_data_func(cls, new_function):
        cls.__call__ = staticmethod(new_function)


access_data_provider = AccessDataProvider()


class AccessControl:
    def __call__(self):
        return access_data_provider()
