class Singleton(type):
    """
    Singleton pattern ensures that even if a class is called several times
    the same class instance is always used.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
