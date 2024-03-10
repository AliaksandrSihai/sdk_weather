
class DuplicateClassError(Exception):
    """Exception raised when trying to create another copies of an object with the same key."""

    pass

class SingletonMeta(type):
    """Metaclass to limit the creation of copies."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
                Override the __call__ method to enforce singleton pattern and prevent duplicate instances.

                Args:
                    cls (type): The class being instantiated.
                    *args: Positional arguments passed to the class constructor.
                    **kwargs: Keyword arguments passed to the class constructor.

                Raises:
                    DuplicateClassError: If an instance with the same key already exists.

                Returns:
                    object: The singleton instance of the class.
                """
        key = kwargs.get("api_key")
        if key in cls._instances:
            raise DuplicateClassError(f"An instance for key '{key}' already exists")
        instance = super().__call__(*args, **kwargs)
        cls._instances[key] = instance
        return instance
